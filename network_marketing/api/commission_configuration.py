from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import CommissionConfiguration
from ..serializers import CommissionConfigurationSerializer
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

class CommissionConfigurationListView(generics.ListAPIView):
    """
    API endpoint that allows CommissionConfiguration to be viewed.
    """
    queryset = CommissionConfiguration.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in CommissionConfiguration._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in CommissionConfiguration._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = CommissionConfigurationSerializer
    ordering = ['id']
    #filterset_fields = {
    #'name': ['exact', 'icontains'],
    #'level':['exact','gt', 'gte', 'lt', 'lte'],
    #'percentage': ['exact','gt', 'gte', 'lt', 'lte'],
    #}

class CommissionConfigurationRetrieveView(generics.RetrieveAPIView):
    queryset = CommissionConfiguration.objects.all()
    serializer_class = CommissionConfigurationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = 'id'

class CommissionConfigurationUpdateView(generics.UpdateAPIView):
    queryset = CommissionConfiguration.objects.all()
    serializer_class = CommissionConfigurationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class CommissionConfigurationDestroyView(generics.DestroyAPIView):
    queryset = CommissionConfiguration.objects.all()
    serializer_class = CommissionConfigurationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class CommissionConfigurationCreateView(generics.CreateAPIView):
    queryset = CommissionConfiguration.objects.all()
    serializer_class = CommissionConfigurationSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  