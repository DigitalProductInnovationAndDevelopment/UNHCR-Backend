from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.user import *
from .views.case import *
from .views.login import *
from .views.signup import *

urlpatterns = [
    path("api/login", loginController, name="login"),
    path("api/signup", signUpController, name="signup"),
    path("api/cases", casesController, name="cases"),
    path("api/cases/<int:id>", caseDetailController, name="caseDetail"),
    path("api/users", usersController, name="users"),
    path("api/users/<int:id>", userDetailController, name="userDetail"),
]
