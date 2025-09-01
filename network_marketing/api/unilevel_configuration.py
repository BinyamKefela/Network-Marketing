from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import UnilevelConfiguration
from ..serializers import UnilevelConfigurationSerializer
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

class UnilevelConfigurationListView(generics.ListAPIView):
    """
    API endpoint that allows UnilevelConfiguration to be viewed.
    """
    queryset = UnilevelConfiguration.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in UnilevelConfiguration._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in UnilevelConfiguration._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = UnilevelConfigurationSerializer
    ordering = ['id']
    #filterset_fields = {
    #'name': ['exact', 'icontains'],
    #'level':['exact','gt', 'gte', 'lt', 'lte'],
    #'percentage': ['exact','gt', 'gte', 'lt', 'lte'],
    #}

class UnilevelConfigurationRetrieveView(generics.RetrieveAPIView):
    queryset = UnilevelConfiguration.objects.all()
    serializer_class = UnilevelConfigurationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class UnilevelConfigurationUpdateView(generics.UpdateAPIView):
    queryset = UnilevelConfiguration.objects.all()
    serializer_class = UnilevelConfigurationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class UnilevelConfigurationDestroyView(generics.DestroyAPIView):
    queryset = UnilevelConfiguration.objects.all()
    serializer_class = UnilevelConfigurationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class UnilevelConfigurationCreateView(generics.CreateAPIView):
    queryset = UnilevelConfiguration.objects.all()
    serializer_class = UnilevelConfigurationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  