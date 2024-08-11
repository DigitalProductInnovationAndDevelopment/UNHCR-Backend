from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.user import *
from .views.userDevice import *
from .views.case import *
from .views.login import *
from .views.message import *
from .views.messageMedia import *
from .views.caseMedia import *
from .views.feedback import *
from .views.signup import *

urlpatterns = [
    path("api/login", loginController, name="login"),
    path("api/signup", signUpController, name="signup"),
    path("api/cases", casesController, name="cases"),
    path("api/cases/<str:id>", caseDetailController, name="caseDetail"),
    path("api/cases/<str:id>/feedback", caseCreateFeedbackController, name="caseCreateFeedback"),
    path("api/cases/<str:id>/messages", messagesController, name="messages"),
    path("api/messages/<str:messageId>/message-media/<str:mediaId>", messageMediaDetailController, name="messageMediaDetail"),
    path("api/cases/<str:caseId>/case-media/<str:mediaId>", caseMediaDetailController, name="caseMediaDetail"),
    path("api/users", usersController, name="users"),
    path("api/users/<str:id>", userDetailController, name="userDetail"),
    path("api/user-devices", userDevicesController, name="userDevices"),
    path("api/user-devices/<str:id>", userDeviceDetailController, name="userDevicesDetail"),
]
