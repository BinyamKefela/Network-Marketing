from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import TreeSetting
from ..serializers import TreeSettingSerializer
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

class TreeSettingListView(generics.ListAPIView):
    """
    API endpoint that allows TreeSetting to be viewed.
    """
    queryset = TreeSetting.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in TreeSetting._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in TreeSetting._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = TreeSettingSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'max_children':['exact'],    
    }

class TreeSettingRetrieveView(generics.RetrieveAPIView):
    queryset = TreeSetting.objects.all()
    serializer_class = TreeSettingSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class TreeSettingUpdateView(generics.UpdateAPIView):
    queryset = TreeSetting.objects.all()
    serializer_class = TreeSettingSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class TreeSettingDestroyView(generics.DestroyAPIView):
    queryset = TreeSetting.objects.all()
    serializer_class = TreeSettingSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class TreeSettingCreateView(generics.CreateAPIView):
    queryset = TreeSetting.objects.all()
    serializer_class = TreeSettingSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  