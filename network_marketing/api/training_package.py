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
    'package__id':['exact'],
    
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_trainings_to_package(request):
    """
    Accepts a list of training IDs and a package ID,
    and associates the trainings with the package.
    Expects JSON payload like:
    {
        "package_id": 1,
        "training_ids": [2, 3, 4]
    }
    """
    if not request.user.has_perm('network_marketing.add_training_package'):
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    package_id = request.data.get("package_id")
    training_ids = request.data.get("training_ids", [])

    try:
        package = TrainingPackage.objects.get(id=package_id)
    except TrainingPackage.DoesNotExist:
        return Response({"detail": "Package not found."}, status=status.HTTP_404_NOT_FOUND)

    created = []
    skipped = []

    # Use transaction so either all succeed or none
    with transaction.atomic():
        for training_id in training_ids:
            try:
                training = TrainingPackage.objects.get(id=training_id)
            except TrainingPackage.DoesNotExist:
                skipped.append({"training_id": training_id, "reason": "Training not found"})
                continue

            obj, was_created = TrainingPackage.objects.get_or_create(
                package=package,
                training=training
            )
            if was_created:
                created.append(training_id)
            else:
                skipped.append({"training_id": training_id, "reason": "Already associated"})

    return Response({
        "created": created,
        "skipped": skipped
    }, status=status.HTTP_200_OK)


  