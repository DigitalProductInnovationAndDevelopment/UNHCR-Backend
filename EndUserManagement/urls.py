from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.user import *
from .views.case import *

urlpatterns = [
    path("api/cases", casesController, name="cases"),
    path("api/cases/<int:id>", caseDetailController, name="caseDetail"),
    path("api/users", usersController, name="users"),
    path("api/users/<int:id>", userDetailController, name="userDetail"),
]
