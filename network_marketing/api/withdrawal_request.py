from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import WithdrawalRequest
from ..serializers import WithdrawalRequestSerializer
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
from django.db import transaction
from ..models import WalletTransaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


load_dotenv()
User = get_user_model()

class WithdrawalRequestListView(generics.ListAPIView):
    """
    API endpoint that allows WithdrawalRequest to be viewed.
    """
    queryset = WithdrawalRequest.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = [field.name for field in WithdrawalRequest._meta.fields if not isinstance(field, ForeignKey)]
    ordering_fields = [field.name for field in WithdrawalRequest._meta.fields if not isinstance(field, ForeignKey)]
    pagination_class = CustomPagination
    serializer_class = WithdrawalRequestSerializer
    ordering = ['id']
    filterset_fields = {
    #'name': ['exact', 'icontains'],
    'user__email':['exact'],
    'user_id':['exact'],
    'status':['exact'],
    
    }

class WithdrawalRequestRetrieveView(generics.RetrieveAPIView):
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    lookup_field = ['id']

class WithdrawalRequestUpdateView(generics.UpdateAPIView):
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'

class WithdrawalRequestDestroyView(generics.DestroyAPIView):
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class WithdrawalRequestCreateView(generics.CreateAPIView):
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['wallet_request_id', 'amount'],
        properties={
            'wallet_request_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
        example={
            "wallet_request_id": 12,
            "amount": 5000
        }
    ),
    responses={
        200: "Successfully approved transaction",
        400: "Invalid request",
        500: "Unexpected error"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_withdrawal_request(request):
    with transaction.atomic():
      wallet_request_id = request.data.get('wallet_request_id')
      amount = request.data.get('amount')
      if (not wallet_request_id) or (not amount):
          return Response({"error":"please provide user_id and amount"},status=status.HTTP_400_BAD_REQUEST)
      try:
          withdrawal_request = WithdrawalRequest.objects.get(id=wallet_request_id)
          user = withdrawal_request.user
          if user.wallet_balance<amount:
              return Response({"error":"withdrawal amount can not exceed wallet balance"},status=status.HTTP_400_BAD_REQUEST)
          withdrawal_request.status = WithdrawalRequest.WITHDRAWAL_REQUEST_CHOICES[1][0]
          wallet_transaction = WalletTransaction()
          wallet_transaction.user = user
          wallet_transaction.amount = amount
          wallet_transaction.type = WalletTransaction.WALLET_TRANSACTION_CHOICES[2][0]
          wallet_transaction.save()
          user.wallet_balance = user.wallet_balance - amount
          user.save
          return Response({"message":"successfully approved transaction"},status=status.HTTP_200_OK)
      except Exception as e:
          return Response({"error":"there was an unexpected error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



  