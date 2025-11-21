from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import NewsPicture
from ..serializers import NewsPictureSerializer
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

class NewsPictureListView(generics.ListAPIView):
    """
    API endpoint that allows NewsPicture to be viewed.
    """
    queryset = NewsPicture.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name','description']
    ordering_fields = [field.name for field in NewsPicture._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = NewsPictureSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'news__description':['exact'],
    'created_at':['exact','lt','lte','gt','gte'],
    'updated_at':['exact','lt','lte','gt','gte']
    
    }

class NewsPictureRetrieveView(generics.RetrieveAPIView):
    queryset = NewsPicture.objects.all()
    serializer_class = NewsPictureSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = 'id'

class NewsPictureUpdateView(generics.UpdateAPIView):
    queryset = NewsPicture.objects.all()
    serializer_class = NewsPictureSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class NewsPictureDestroyView(generics.DestroyAPIView):
    queryset = NewsPicture.objects.all()
    serializer_class = NewsPictureSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class NewsPictureCreateView(generics.CreateAPIView):
    queryset = NewsPicture.objects.all()
    serializer_class = NewsPictureSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  