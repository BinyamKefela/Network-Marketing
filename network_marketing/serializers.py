from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User,Group,Permission,ContentType
from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from .models import *
from auditlog.models import LogEntry


User = get_user_model()


#this is a class used to customize the JWT token obtaining since we need to send the permission list to the user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
        # Add custom claims
        #token['username'] = user.username
        token['email'] = user.email
        #token['first_name'] = user.first_name
        #token['last_name'] = user.last_name
        #token['company'] = user.company.id if user.company else None
        return token

    username_field = "email"
    
    def validate(self, attrs):
        credentials={
            "email":attrs.get("email"),
            "password":attrs.get("password")
        }
    
        data = super().validate(attrs)
        user = authenticate(email=attrs['email'],password=attrs['password'])
        if user and not user.is_active:
            raise serializers.ValidationError({"error":"user is banned from the system"})
           
    

        user = authenticate(**credentials)
        
        if user is None:
            raise serializers.ValidationError({"error":"invalid credentials"})
        
        #lets add permissions to the token payload
        #permissions = user.get_all_permissions()
        data = super().validate(attrs)
        data['permissions'] = list(user.get_all_permissions())
        #data['company'] = user.company.id if user.company else None
        data['email'] = user.email
        data['user'] = user.id
        data['groups'] = list(user.groups.values_list('name',flat=True))
        data['referal_code'] = user.referal_code
        return data


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)
    user_permissions = serializers.SlugRelatedField(slug_field="codename",queryset=Permission.objects.all(),many=True,required=False)
    groups = serializers.SlugRelatedField(slug_field="name",queryset=Group.objects.all(),many=True,required=False)
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        if self.instance is None and "password" not in data:
            raise serializers.ValidationError({"password":"This field is required when creating a new user!"})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password",None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password",None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Ensure superusers receive all permissions."""
        representation = super().to_representation(instance)

        if instance.is_superuser:
            # Get all permission codenames for superusers
            all_permissions = Permission.objects.values_list("codename", flat=True)
            representation["user_permissions"] = list(all_permissions)
        else:
            # Regular users: only show explicitly assigned permissions
            representation["user_permissions"] = list(instance.user_permissions.values_list("codename", flat=True))
        #representation['company'] = CompanySerializerForUser(instance.company).data
        #representation['subscriptions'] = SubscriptionSerializerForUser(Subscription.objects.filter(company=instance.company),many=True).data
        return representation
    
    def get_profile_picture(self,obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        elif obj.profile_picture:
            # fallback if no request is available
            from django.conf import settings
            return settings.SITE_URL + obj.profile_picture.url
        return None


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(slug_field="codename",queryset=Permission.objects.all(),many=True,required=False)

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(write_only=True,queryset=ContentType.objects.all())
    class Meta:
        model = Permission
        fields = "__all__"


class MlmSettingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MlmSetting
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"


class CommissionConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommissionConfiguration
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = "__all__"


class CommissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commission
        fields = "__all__"


class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"

class HousingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Housing
        fields = "__all__"

class PromoterBuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoterBuyer
        fields = "__all__"


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = "__all__"

class TrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = "__all__"

class ProductPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPackage
        fields = "__all__"

class TrainingPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingPackage
        fields = "__all__"


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = "__all__"



