from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import *
from ..serializers import SaleSerializer
from network_marketing.api.custom_pagination import CustomPagination
import datetime
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view,permission_classes
from dotenv import load_dotenv
from django.db.models import ForeignKey


load_dotenv()
User = get_user_model()

class SaleListView(generics.ListAPIView):
    """
    API endpoint that allows Sale to be viewed.
    """
    queryset = Sale.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Sale._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in Sale._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = SaleSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'product__id':['exact'],
    'product__name':['exact'],
    'buyer__email':['exact'],
    'seller__email':['exact'],
    'payment_date': ['exact','gt', 'gte', 'lt', 'lte'],
    'sub_total': ['exact','gt', 'gte', 'lt', 'lte'],
    }

class SaleRetrieveView(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class SaleUpdateView(generics.UpdateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class SaleDestroyView(generics.DestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_sale(request):
    seller = request.data.get('seller')
    buyer = request.data.get('buyer')
    payment_date = request.data.get('payment_date')
    product = request.data.get('product')
    quantity = request.data.get('quantity')
    package = request.data.get('package')
    

    if not (seller or buyer or payment_date or (product or package) or quantity):
        return Response({"error":"please make sure you sent seller, buyer, payment_date, product, package, and quantity"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        seller = User.objects.get(id=seller)
        try:
            buyer = User.objects.get('buyer')
            if package:
                try:
                   package = Package.objects.get('package')
                except:
                   return Response({"error":"there is no package with the given package id"})
            if product:
                try:
                   product = Product.objects.get('product')
                except:
                   return Response({"error":"there is no product with the given product id"})
        except:
            return Response({"error":"there is no user with the given buyer id"})
    except:
        return Response({"error":"There is no user with the given seller id"})
    
    sale = Sale()
    if product:
       sale.product = product
       price = product.price
    if package:
       sale.package = package
       price = package.price
    sale.seller = seller
    sale.buyer = buyer
    sale.quantity = quantity
    sale.price = price
    sale.sub_total = sale.quantity*sale.price
    sale.payment_date = payment_date
    sale.status = Sale.SALE_STATUS[0]
    sale.save()

    #the level of the seller is taken
    i=seller.level
    mlm_setting = MlmSetting.objects.all().first()
    # the max level commissions are calculated 
    j = mlm_setting.max_level
    while i>0 and j>0 :


        try:
            commission_configuration = CommissionConfiguration.objects.get(level = i,category=product.category)
        except:
            return Response({"error":"There is no commssion configuration for the given sellers level and product category"})
        
    
        #create commission from the sale for the seller 
        commission = Commission()
        commission.sale = sale
        commission.amount = commission_configuration.percentage*sale.sub_total
        commission.save()
    
        #mlm_settng = MlmSetting.objects.all().first()
    
        #if mlm_settng.max_level>=buyer.level:
        
        try:
            commisioned_user = User.objects.filter(referal_code=buyer.referal_code).first()
            if j != mlm_setting.max_level:
               commissioned_user = User.objects.filter(referal_code = commisioned_user.referal_code).first()
        except:
            return Response({"error":"there is no seller with the given referal code"})
        wallet_transaction_seller = WalletTransaction()
        wallet_transaction_seller.user = commisioned_user
        wallet_transaction_seller.amount = commission.amount
        wallet_transaction_seller.type = WalletTransaction.WALLET_TRANSACTION_CHOICES[0]
        wallet_transaction_seller.reference = commission
        wallet_transaction_seller.save()

        if j == mlm_setting.max_level:
           wallet_transaction_buyer = WalletTransaction()
           wallet_transaction_buyer.user = buyer
           wallet_transaction_buyer.amount = sale.sub_total
           wallet_transaction_buyer.type = WalletTransaction.WALLET_TRANSACTION_CHOICES[1]
           wallet_transaction_buyer.save()
    
        seller.wallet_balance += commission.amount
        seller.save()
        j = j-1
    
    
    return Response({"message":"successfully saved sales data!"},status=status.HTTP_201_CREATED)
    



from django.db import transaction

from ..models import (
    User, Product, Package, Sale, Commission,
    WalletTransaction, UnilevelConfiguration, MlmSetting, TreeSetting,
)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_sale_new(request):
    """
    Handles a post-sale event, records the sale, and distributes commissions 
    up the ternary tree hierarchy.
    """
    data = request.data
    seller_id = data.get('seller')
    buyer_id = data.get('buyer')
    product_id = data.get('product')
    package_id = data.get('package')
    quantity = data.get('quantity')
    
    # 1. Input Validation and Data Retrieval
    if not all([seller_id, buyer_id, quantity]):
        return Response(
            {"error": "Please provide seller, buyer, and quantity."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not (product_id or package_id):
        return Response(
            {"error": "Please provide either a product or a package."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        seller = User.objects.get(id=seller_id)
        buyer = User.objects.get(id=buyer_id)
        
        # Determine the item and price based on product or package
        item = None
        category = None
        if product_id:
            item = Product.objects.get(id=product_id)
            sale_price = item.price
            category = item.category
        elif package_id:
            item = Package.objects.get(id=package_id)
            sale_price = item.price
            category = item.category
        
        total_price = sale_price * int(quantity)
        
        # Get MLM settings and commission configuration
        mlm_settings = MlmSetting.objects.first()
        commission_config = CommissionConfiguration.objects.first()
        
        if not mlm_settings:
            return Response(
                {"error": "MLM settings not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if not commission_config:
            return Response(
                {"error": "Commission configuration not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    except Package.DoesNotExist:
        return Response({"error": "Package not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate the total commission pool from the unilevel_bonus
    total_commission_pool = total_price * (commission_config.unilevel_bonus / 100)

    # Use a database transaction to ensure atomicity
    with transaction.atomic():
        # 2. Record the sale
        sale = Sale.objects.create(
            product=item if isinstance(item, Product) else None,
            package=item if isinstance(item, Package) else None,
            seller=seller,
            buyer=buyer,
            quantity=quantity,
            price=sale_price,
            sub_total=total_price,
            payment_date=data.get('payment_date'),
            status='commision recorded'
        )

        # 3. Distribute commissions up the hierarchy
        current_upline_user = buyer.recruited_by
        level = 1

        while current_upline_user and level <= mlm_settings.max_level:
            try:
                # Find commission percentage for the current level and category
                config = UnilevelConfiguration.objects.get(level=level)
                
                # Calculate the individual commission from the total commission pool
                commission_amount = total_commission_pool * (config.percentage / 100)

                # 4. Create a commission record
                commission = Commission.objects.create(
                    sale=sale,
                    amount=commission_amount
                )

                # 5. Create a wallet transaction and update user's balance
                WalletTransaction.objects.create(
                    user=current_upline_user,
                    amount=commission_amount,
                    type='credit',
                    reference=commission
                )
                
                # Update user's wallet balance
                current_upline_user.wallet_balance += commission_amount
                current_upline_user.save()

                # Move to the next level up the tree
                current_upline_user = current_upline_user.recruited_by
                level += 1
            
            except UnilevelConfiguration.DoesNotExist:
                # Stop if no configuration is found for this level/category
                break
            except Exception as e:
                # Rollback the transaction and return an error
                transaction.set_rollback(True)
                return Response(
                    {"error": f"An error occurred during commission calculation: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    return Response(
        {"message": "Sale successfully recorded and commissions distributed."},
        status=status.HTTP_201_CREATED
    )
