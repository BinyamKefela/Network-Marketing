from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Sale
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


  