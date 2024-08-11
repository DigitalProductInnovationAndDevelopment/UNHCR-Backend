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
    Gets a user. It is designed for users to get info about their own accounts.
    @Endpoint: /users
    """

    user = kwargs["loggedUser"]
    # The case for end user tring to operate on another user except himself/herself
    # Use admin endpoints for operating on other users
    if not user:
        return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    try: 
        responseSerializer = UserGetResponseSerializer(user)
        return Response(
            {"success": True, "data": responseSerializer.data},
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"success": False, "message": translationService.translate('user.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('general.exception.message')},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )
