from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Commission
from ..serializers import CommissionSerializer
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

class CommissionListView(generics.ListAPIView):
    """
    API endpoint that allows Commission to be viewed.
    """
    queryset = Commission.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in Commission._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in Commission._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = CommissionSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'sale__id':['exact'],
    'sale__product__id':['exact'],
    'sale__product__name':['exact','icontains'],
    #'buyer__email':['exact'],
    #'seller__email':['exact'],
    'amount': ['exact','gt', 'gte', 'lt', 'lte'],
    }

class CommissionRetrieveView(generics.RetrieveAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class CommissionUpdateView(generics.UpdateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class CommissionDestroyView(generics.DestroyAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class CommissionCreateView(generics.CreateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  