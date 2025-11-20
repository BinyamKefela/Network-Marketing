from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import ProductPackage
from ..serializers import ProductPackageSerializer
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
from django.db import IntegrityError, transaction



load_dotenv()

class ProductPackageListView(generics.ListAPIView):
    """
    API endpoint that allows ProductPackage to be viewed.
    """
    queryset = ProductPackage.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name','description']
    ordering_fields = [field.name for field in ProductPackage._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = ProductPackageSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'package__id':['exact'],
    
    }

class ProductPackageRetrieveView(generics.RetrieveAPIView):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = 'id'

class ProductPackageUpdateView(generics.UpdateAPIView):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class ProductPackageDestroyView(generics.DestroyAPIView):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class ProductPackageCreateView(generics.CreateAPIView):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


# views.py
from django.db import IntegrityError, transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status

from ..models import ProductPackage, Product, Package

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_products_to_package(request):
    """
    Accepts a list of product IDs and a package ID,
    creates ProductPackage instances accordingly.
    Example body:
    {
        "package_id": 1,
        "product_ids": [2, 3, 4]
    }
    """
    if not request.user.has_perm('network_marketing.add_productpackage'):
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    package_id = request.data.get("package_id")
    product_ids = request.data.get("product_ids", [])

    if not package_id or not isinstance(product_ids, list):
        return Response(
            {"detail": "package_id and product_ids (list) are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        return Response({"detail": "Package not found."}, status=status.HTTP_404_NOT_FOUND)

    created = []
    skipped = []

    ProductPackage.objects.filter(package=package).delete()

    # Use transaction so either all succeed or none
    with transaction.atomic():
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                obj, created_flag = ProductPackage.objects.get_or_create(
                    product=product, package=package
                )
                if created_flag:
                    created.append(product_id)
                else:
                    skipped.append(product_id)
            except Product.DoesNotExist:
                skipped.append(product_id)
            except IntegrityError:
                skipped.append(product_id)

    return Response(
        {
            "created": created,
            "skipped": skipped,
            "message": f"{len(created)} products linked to package {package_id}, {len(skipped)} skipped.",
        },
        status=status.HTTP_201_CREATED,
    )



  