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
    path("api/cases/<int:id>", caseDetailController, name="caseDetail"),
    path("api/cases/<int:id>/feedback", caseCreateFeedbackController, name="caseCreateFeedback"),
    path("api/cases/<int:id>/messages", messagesController, name="messages"),
    path("api/messages/<int:messageId>/message-media/<str:mediaId>", messageMediaDetailController, name="messageMediaDetail"),
    path("api/cases/<int:caseId>/case-media/<str:mediaId>", caseMediaDetailController, name="caseMediaDetail"),
    path("api/users", usersController, name="users"),
    path("api/users/<int:id>", userDetailController, name="userDetail"),
    path("api/user-devices", userDevicesController, name="userDevices"),
    path("api/user-devices/<int:id>", userDeviceDetailController, name="userDevicesDetail"),
]
