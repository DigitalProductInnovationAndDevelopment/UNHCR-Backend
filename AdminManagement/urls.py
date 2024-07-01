from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.user import *
from .views.case import *

urlpatterns = [
    path("api/admin/users", adminUsersController, name="adminUsers"),
    path("api/admin/users/<int:id>", adminUserDetailController, name="adminUserDetail"),
    path("api/admin/cases", adminCasesController, name="adminCases"),
    path("api/admin/cases/<int:id>", adminCaseDetailController, name="adminCaseDetail"),
     path("api/admin/user-devices", adminUserDevicesController, name="adminUserDevices"),
    path("api/admin/user-devices/<int:id>", adminUserDevicesDetailController, name="adminUserDevicesDetail"),
]
