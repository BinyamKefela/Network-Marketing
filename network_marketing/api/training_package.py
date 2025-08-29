from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import TrainingPackage
from ..serializers import TrainingPackageSerializer
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

class TrainingPackageListView(generics.ListAPIView):
    """
    API endpoint that allows TrainingPackage to be viewed.
    """
    queryset = TrainingPackage.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name','description']
    ordering_fields = [field.name for field in TrainingPackage._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = TrainingPackageSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'name':['exact'],
    
    }

class TrainingPackageRetrieveView(generics.RetrieveAPIView):
    queryset = TrainingPackage.objects.all()
    serializer_class = TrainingPackageSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class TrainingPackageUpdateView(generics.UpdateAPIView):
    queryset = TrainingPackage.objects.all()
    serializer_class = TrainingPackageSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class TrainingPackageDestroyView(generics.DestroyAPIView):
    queryset = TrainingPackage.objects.all()
    serializer_class = TrainingPackageSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class TrainingPackageCreateView(generics.CreateAPIView):
    queryset = TrainingPackage.objects.all()
    serializer_class = TrainingPackageSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  