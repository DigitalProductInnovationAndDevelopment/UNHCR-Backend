import os
import traceback
import logging
import json

from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "POST"])
def usersController(request, **kwargs):

    if request.method == "GET":
        """
        Lists all users.
        @Endpoint: /users
        """
        try:
            # The users can only be listed via the admin user list endpoint.
            return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "POST":
        """
        Creates a user.
        @Endpoint: /users
        """
        try:
            # The users can only be created via the sign up endpoint. For direct creation, use admin user create.
            return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )
