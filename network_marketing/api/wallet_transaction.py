from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import WalletTransaction
from ..serializers import WalletTransactionSerializer
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

class WalletTransactionListView(generics.ListAPIView):
    """
    API endpoint that allows WalletTransaction to be viewed.
    """
    queryset = WalletTransaction.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in WalletTransaction._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in WalletTransaction._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = WalletTransactionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'reference__sale__id':['exact'],
    'reference__sale__product__id':['exact'],
    'reference__sale__product__name':['exact'],
    'user__email':['exact'],
    'type':['exact'],
    'amount': ['exact','gt', 'gte', 'lt', 'lte'],
    }

class WalletTransactionRetrieveView(generics.RetrieveAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class WalletTransactionUpdateView(generics.UpdateAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class WalletTransactionDestroyView(generics.DestroyAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class WalletTransactionCreateView(generics.CreateAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  