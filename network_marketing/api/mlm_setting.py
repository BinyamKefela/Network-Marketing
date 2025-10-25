from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import MlmSetting
from ..serializers import MlmSettingSerializer
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

class MlmSettingListView(generics.ListAPIView):
    """
    API endpoint that allows MlmSetting to be viewed.
    """
    queryset = MlmSetting.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['max_level','min_withdrawal_amount','payout_frequency']
    ordering_fields = [field.name for field in MlmSetting._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = MlmSettingSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'max_level':['exact','gt', 'gte', 'lt', 'lte'],
    'business_volume_amount_in_sales': ['exact','gt', 'gte', 'lt', 'lte'],
    'payout_frequency': ['exact','gt', 'gte', 'lt', 'lte'],
    }

class MlmSettingRetrieveView(generics.RetrieveAPIView):
    queryset = MlmSetting.objects.all()
    serializer_class = MlmSettingSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class MlmSettingUpdateView(generics.UpdateAPIView):
    queryset = MlmSetting.objects.all()
    serializer_class = MlmSettingSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class MlmSettingDestroyView(generics.DestroyAPIView):
    queryset = MlmSetting.objects.all()
    serializer_class = MlmSettingSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class MlmSettingCreateView(generics.CreateAPIView):
    queryset = MlmSetting.objects.all()
    serializer_class = MlmSettingSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  