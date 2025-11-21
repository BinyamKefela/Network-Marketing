from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import EventPicture
from ..serializers import EventPictureSerializer
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

class EventPictureListView(generics.ListAPIView):
    """
    API endpoint that allows EventPicture to be viewed.
    """
    queryset = EventPicture.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name','description']
    ordering_fields = [field.name for field in EventPicture._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = EventPictureSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'event__description':['exact'],
    'event__start_date':['exact','lt','lte','gt','gte'],
    'event__end_date':['exact','lt','lte','gt','gte'],
    'created_at':['exact','lt','lte','gt','gte'],
    'updated_at':['exact','lt','lte','gt','gte']
    
    }

class EventPictureRetrieveView(generics.RetrieveAPIView):
    queryset = EventPicture.objects.all()
    serializer_class = EventPictureSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = 'id'

class EventPictureUpdateView(generics.UpdateAPIView):
    queryset = EventPicture.objects.all()
    serializer_class = EventPictureSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class EventPictureDestroyView(generics.DestroyAPIView):
    queryset = EventPicture.objects.all()
    serializer_class = EventPictureSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class EventPictureCreateView(generics.CreateAPIView):
    queryset = EventPicture.objects.all()
    serializer_class = EventPictureSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


  