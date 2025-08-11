from django.db import models

from django.contrib.auth.models import  AbstractUser,AbstractBaseUser,BaseUserManager,PermissionsMixin,Group
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from datetime import timedelta

import uuid
from auditlog.registry import auditlog

# Create your models here.

def validate_uploaded_image_extension(value):
    valid_extensions = ['.png','.jpg','.jpeg','.PNG','.JPG','.JPEG']
    ext = os.path.splitext(value.name)[1]
    if not ext in valid_extensions:
        raise ValidationError('Unsupported filed extension')
        

def get_upload_path(instance,filename):
    ext = filename.split('.')[-1]
    new_file_name = "profiles/"+f'{instance.id}.{ext}'
    return new_file_name

# Custom manager for user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='company_owner')
    calendar_type = models.CharField(
        max_length=10, 
        choices=[('GREGORIAN', 'Gregorian'), ('ETHIOPIAN', 'Ethiopian')],
        default='GREGORIAN'
    )
    base_currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    company_type = models.CharField(choices=[('private', 'private'), ('public', 'public'),('military and public','military and public')], max_length=100, default='Private')
    
    
    def __str__(self):
        return self.name
    

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,null=True)
    middle_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    profile_picture = models.FileField(upload_to=get_upload_path,validators=[validate_uploaded_image_extension],null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    is_company_admin = models.BooleanField(default=False)

    # Make groups and user_permissions optional by adding blank=True and null=True
    groups = models.ManyToManyField(
        'auth.Group', 
        blank=True,
        null=True, 
        related_name='customuser_set', 
        related_query_name='customuser', 
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        blank=True,
        null=True, 
        related_name='customuser_set', 
        related_query_name='customuser', 
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # fields to be used when creating a superuser
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        return super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('email', 'company')


auditlog.register(User)


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.user.email}"


class EmailResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)


class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Configuration(models.Model):
    Company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rank(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    property = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False)
    image = models.ImageField(upload_to="properties")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Housing(models.Model):
    code = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Promoter(models.Model):
    user = models.CharField(max_length=100)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromoterHousing(models.Model):
    promoter = models.ForeignKey(Promoter,on_delete=models.CASCADE,null=False,blank=False)
    housing = models.ForeignKey(Housing,on_delete=models.CASCADE,null=False,blank=False)
    total_accumulated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class productPayment(models.Model):
    promoter = models.ForeignKey(Promoter,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transction_id = models.CharField(max_length=200,unique=True,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromoterTransaction(models.Model):
    TRANSACTION_TYPES = (("PRODUCT PURCHASE","PRODUCT PURCHASE"),
                         ("CHILD COMMISION","CHILD COMMISION"),
                         ("MATCHING COMMISSION","MATCHING COMMISION"))
    Promoter = models.ForeignKey(Promoter,on_delete=models.SET_NULL,null=True,blank=True)
    transaction_type = models.CharField(max_length=200,choices=TRANSACTION_TYPES)
    in_amount = models.DecimalField(max_digits=10, decimal_places=2)
    out_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompanyTransaction(models.Model):
    TRANSACTION_TYPES = (("PROMOTER PAYMENT","PROMOTER PAYMENT"),
                         ("CHILD COMMISION","CHILD COMMISION"),
                         ("MATCHING PAYMENT","MATCHING PAYMENT"))
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True,blank=True)
    transaction_type = models.CharField(max_length=200,choices=TRANSACTION_TYPES)
    in_amount = models.DecimalField(max_digits=10, decimal_places=2)
    out_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompanyBalance(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class PromoterParentChild(models.Model):
    child = models.ForeignKey(Promoter,on_delete=models.CASCADE,null=False,blank=False,related_name='promoter_child')
    parent = models.ForeignKey(Promoter,on_delete=models.CASCADE,null=False,blank=True,related_name='promoter_parent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubscriptionPlan(models.Model):
    SERVICES_INCLUDED = [
        ('HR Management', 'HR Management'),
        ('Payroll Management', 'Payroll Management'),
        ('Attendance Tracking', 'Attendance Tracking'),
        ('Leave Management', 'Leave Management'),
        ('Performance Reviews', 'Performance Reviews'),
        ('Recruitment', 'Recruitment'),
        ('Training Management', 'Training Management'),
        ('Document Management', 'Document Management'),
        ('Employee Self-Service Portal', 'Employee Self-Service Portal'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    #services_included = models.CharField(max_length=255, blank=True,choices=SERVICES_INCLUDED)
    #price = models.DecimalField(max_digits=10, decimal_places=2)
    max_users = models.PositiveIntegerField(default=0)
    duration_months = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"
    
    class Meta:
        unique_together = ('company',)


def validate_subscription_payment_picture(value):
    valid_extensions = ['.png','.jpg','.jpeg','.PNG','.JPG','.JPEG']
    ext = os.path.splitext(value.name)[1]
    if not ext in valid_extensions:
        raise ValidationError('Unsupported filed extension')
        

def get_subscription_payment_image_upload_path(instance,filename):
    new_file_name = "subscription_payments/"+f'{filename}'
    return new_file_name


class SubscriptionPayment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    image = models.FileField(upload_to=get_subscription_payment_image_upload_path,validators=[validate_subscription_payment_picture],null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    #payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer'), ('Other', 'Other')])
    transaction_id = models.CharField(max_length=100, unique=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subscription.company.name} - {self.amount} on {self.payment_date}"