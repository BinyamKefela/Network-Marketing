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
    'amount': ['exact','gt', 'gte', 'lt', 'lte'],
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
    

    if not (seller or buyer):
        return Response({"error":"please make sure you sent seller, buyer, payment_date, product, and quantity"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        seller = User.objects.get(id=seller)
        try:
            buyer = User.objects.get('buyer')
            try:
                product = Product.objects.get('product')
            except:
                return Response({"error":"there is no product with the given product id"})
        except:
            return Response({"error":"there is no user with the given seller id"})
    except:
        return Response({"error":"There is no user with the given buyer id"})
    
    try:
        commission_configuration = CommissionConfiguration.objects.get(level = seller.level,category=product.category)
    except:
        return Response({"error":"There is no commssion configuration for the given sellers level and product category"})
    sale = Sale()
    sale.product = product
    sale.seller = seller
    sale.buyer = buyer
    sale.quantity = quantity
    sale.price = product.price
    sale.sub_total = sale.quantity*sale.price
    sale.payment_date = payment_date
    sale.status = Sale.SALE_STATUS[0]
    sale.save()

    commission = Commission()
    commission.sale = sale
    commission.amount = commission_configuration.percentage*sale.sub_total
    commission.save()

    mlm_settng = MlmSetting.objects.all().first()

    if mlm_settng.max_level>=buyer.level:

       wallet_transaction_seller = WalletTransaction()
       wallet_transaction_seller.user = seller
       wallet_transaction_seller.amount = commission.amount
       wallet_transaction_seller.type = WalletTransaction.WALLET_TRANSACTION_CHOICES[0]
       wallet_transaction_seller.reference = commission
       wallet_transaction_seller.save()

    wallet_transaction_buyer = WalletTransaction()
    wallet_transaction_buyer.user = buyer
    wallet_transaction_buyer.amount = sale.sub_total
    wallet_transaction_buyer.type = WalletTransaction.WALLET_TRANSACTION_CHOICES[1]
    wallet_transaction_buyer.save()

    seller.wallet_balance = commission.amount
    seller.save()


    return Response({"message":"successfully saved sales data!"},status=status.HTTP_201_CREATED)
    