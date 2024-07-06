from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from .views.user import *
from .views.case import *
from .views.message import *
from .views.media import *
urlpatterns = [
    path("api/cases", casesController, name="cases"),
    path("api/cases/<int:id>", caseDetailController, name="caseDetail"),
    path("api/users", usersController, name="users"),
    path("api/messages", messageController, name="messages"),
    path("api/users/<int:id>", userDetailController, name="userDetail"),
    path("api/media", mediaController, name="media"),
]
