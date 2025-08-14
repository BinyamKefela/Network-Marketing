
from django.contrib import admin
from django.urls import path
from django.urls import include
from .api.user import *
from .api.group import *
from .api.permission import *
from .api.mlm_setting import *
from .api.category import *
from .api.commission_configuration import *
from .api.product import *
from .api.sale import *
from .api.commision import *
from .api.wallet_transaction import *

urlpatterns = [

  #--------------------------------users routes-----------------------------------------------
  path("get_users", UserListView.as_view(), name="get_users"),
  path("get_user/<int:id>",UserRetrieveView.as_view(),name='get_user'),
  path("post_user",UserCreateView.as_view(),name="post_user"),
  path("update_user/<int:id>",update_user,name="new_update_user"),
  path("deactivate_user/<int:id>",UserDestroyView.as_view(),name="delete_user"),
  path("set_user_permissions",setUserPermissions,name="set_user_permissions"),
  path("set_user_groups", setUserGroups, name="set_user_group"),
  path("send_password_reset_email",send_password_reset_email,name="send_password_reset_email"),
  path("reset_password/<str:token>",reset_password,name="reset_passord"),
  path("get_user_profile",get_user_profile,name="get_user_id"),
  path("activate_user/<int:id>", activate_user, name="activate_user"),
  #path("get_owners",get_owners,name="get_owners"),
  #path("get_managers",get_managers,name="get_managers"),
  #path("get_owners",GetOwners.as_view(),name="get_owners"),

  path('auth/google', GoogleAuthView.as_view(), name='google_auth'),


  path('sign_up',sign_up, name='sign_up'),
  path('verify-email/<uuid:token>', verify_email, name='verify_email'),

  path('send_password_reset_email_phone',send_password_reset_email_phone, name='send_password_reset_email_phone'),
  path('verify_reset_code', VerifyResetCodeView.as_view(), name='verify_reset_code'),
  path('reset_password_phone',reset_password_phone,name='reset_password_phone'),

  path("change_password",change_password,name="change_password"),


  #--------------------------------Groups routes----------------------------------------------
  path("get_groups", GroupListView.as_view(), name="get_groups"),
  path("get_group/<int:id>",GroupRetrieveView.as_view(),name='get_group'),
  path("post_group",GroupCreateView.as_view(),name="post_group"),
  path("update_group/<int:id>",GroupUpdateView.as_view(),name="update_group"),
  path("delete_group/<int:id>",GroupDestroyView.as_view(),name="delete_group"),
  path("set_group_permissions",setGroupPermissions,name="set_group_permissions"),
  path("get_group_permissions",getGroupPermission,name="get_group_permissions"),


#--------------------------------Permission routes--------------------------------------------
  path("get_permissions", PermissionListView.as_view(), name="get_permissions"),
  path("get_permission/<int:id>",PermissionRetrieveView.as_view(),name='get_permission'),
  path("post_permission",PermissionCreateView.as_view(),name="post_permission"),
  path("update_permission/<int:id>",PermissionUpdateView.as_view(),name="update_permission"),
  path("delete_permission/<int:id>",PermissionDestroyView.as_view(),name="delete_permission"),


#---------------------------------Mlm settings routes------------------------------------------
path("get_mlm_settings", MlmSettingListView.as_view(), name="get_mlm_settings"),
path("get_mlm_setting/<int:id>", MlmSettingRetrieveView.as_view(), name="get_mlm_setting"),
path("post_mlm_setting", MlmSettingCreateView.as_view(), name="post_mlm_setting"),
path("update_mlm_setting/<int:id>", MlmSettingUpdateView.as_view(), name="update_mlm_setting"),
path("delete_mlm_setting/<int:id>", MlmSettingDestroyView.as_view(), name="delete_mlm_setting"),


#---------------------------------Category routes------------------------------------------
path("get_categories", CategoryListView.as_view(), name="get_categories"),
path("get_category/<int:id>", CategoryRetrieveView.as_view(), name="get_category"),
path("post_category", CategoryCreateView.as_view(), name="post_category"),
path("update_category/<int:id>", CategoryUpdateView.as_view(), name="update_category"),
path("delete_category/<int:id>", CategoryDestroyView.as_view(), name="delete_category"),


#---------------------------------Product routes------------------------------------------
path("get_products", ProductListView.as_view(), name="get_products"),
path("get_product/<int:id>", ProductRetrieveView.as_view(), name="get_product"),
path("post_product", ProductCreateView.as_view(), name="post_product"),
path("update_product/<int:id>", ProductUpdateView.as_view(), name="update_product"),
path("delete_product/<int:id>", ProductDestroyView.as_view(), name="delete_product"),


#---------------------------------Commission Configuration routes------------------------------------------
path("get_commission_configurations", CommissionConfigurationListView.as_view(), name="get_commission_configurations"),
path("get_commission_configuration/<int:id>", CommissionConfigurationRetrieveView.as_view(), name="get_commission_configuration"),
path("post_commission_configuration", CommissionConfigurationCreateView.as_view(), name="post_commission_configuration"),
path("update_commission_configuration/<int:id>", CommissionConfigurationUpdateView.as_view(), name="update_commission_configuration"),
path("delete_commission_configuration/<int:id>", CommissionConfigurationDestroyView.as_view(), name="delete_commission_configuration"),

#---------------------------------Sale routes------------------------------------------
path("get_sales", SaleListView.as_view(), name="get_sales"),
path("get_sale/<int:id>", SaleRetrieveView.as_view(), name="get_sale"),
path("post_sale", SaleCreateView.as_view(), name="post_sale"),
path("update_sale/<int:id>", SaleUpdateView.as_view(), name="update_sale"),
path("delete_sale/<int:id>", SaleDestroyView.as_view(), name="delete_sale"),

#---------------------------------Commission routes------------------------------------------
path("get_commissions", CommissionListView.as_view(), name="get_commissions"),
path("get_commission/<int:id>", CommissionRetrieveView.as_view(), name="get_commission"),
path("post_commission", CommissionCreateView.as_view(), name="post_commission"),
path("update_commission/<int:id>", CommissionUpdateView.as_view(), name="update_commission"),
path("delete_commission/<int:id>", CommissionDestroyView.as_view(), name="delete_commission"),

#---------------------------------WalletTransaction routes------------------------------------------
path("get_wallet_transactions", WalletTransactionListView.as_view(), name="get_wallet_transactions"),
path("get_wallet_transaction/<int:id>", WalletTransactionRetrieveView.as_view(), name="get_wallet_transaction"),
path("post_wallet_transaction", WalletTransactionCreateView.as_view(), name="post_wallet_transaction"),
path("update_wallet_transaction/<int:id>", WalletTransactionUpdateView.as_view(), name="update_wallet_transaction"),
path("delete_wallet_transaction/<int:id>", WalletTransactionDestroyView.as_view(), name="delete_wallet_transaction"),



]
