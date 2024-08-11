from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.message import *
from .views.user import *
from .views.case import *
from .views.userDevice import *

urlpatterns = [
    path("api/admin/users", adminUsersController, name="adminUsers"),
    path("api/admin/users/<str:id>", adminUserDetailController, name="adminUserDetail"),
    path("api/admin/cases", adminCasesController, name="adminCases"),
    path("api/admin/cases/<str:id>", adminCaseDetailController, name="adminCaseDetail"),
    path("api/admin/user-devices", adminUserDevicesController, name="adminUserDevices"),
    path("api/admin/user-devices/<str:id>", adminUserDeviceDetailController, name="adminUserDevicesDetail"),
    path("api/admin/<str:id>/messages", adminMessagesController, name="adminMessages"),
]
