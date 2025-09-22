from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import OrderingFilter,SearchFilter
from ..models import Rank,TreeSetting
from ..serializers import CommissionSerializer
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

User = get_user_model()


RANKS_AVAILABLE = Rank.objects.all()


def upgrade_rank(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    
    
    if user.rank.name == "Vision Builder":
        make_growth_builder(user_id)
    
    if user.rank.name == "Growth partner":
        make_team_leader(user_id)
    
    if user.rank.name == "Team Leader":
        make_impact_mentor(user_id)
    
    if user.rank.name == "Impact Mentor":
        make_strategic_director(user_id)
    
    if user.rank.name == "Strategic Director":
        make_global_influencer(user_id)
    
    if user.rank.name == "Global Influencer":
        make_legacy_share_holder(user_id)


def make_growth_builder(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Vision Builder").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Growth partner')
        user.save()



def make_team_leader(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Growth partner").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Team Leader')
        user.save()



def make_impact_mentor(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Team Leader").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Impact Mentor')
        user.save()



def make_strategic_director(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Impact Mentor").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Strategic Director')
        user.save()



def make_global_influencer(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Strategic Director").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Global Influencer')
        user.save()



def make_legacy_share_holder(user_id):
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    if User.objects.filter(recruited_by=user,rank__name="Global Influencer").count() >= TreeSetting.objects.first().max_children:
        user.rank = Rank.objects.get(name='Legacy Shareholder')
        user.save()

  