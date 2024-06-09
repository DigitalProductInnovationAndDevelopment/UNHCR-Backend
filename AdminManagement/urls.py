from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.user import *

urlpatterns = [
    path("api/users", adminUsersController, name="adminUsers"),
    path("api/users/<int:id>", adminUserDetailController, name="adminUserDetail"),
]
