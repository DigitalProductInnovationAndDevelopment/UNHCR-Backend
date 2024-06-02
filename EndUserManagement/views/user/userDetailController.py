import traceback
import logging

from EndUserManagement.models import User
from EndUserManagement.services import (
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
@api_view(["GET", "PUT", "DELETE"])
def userDetailController(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a user.
        @Endpoint: /users/:id
        """
        try:
            return Response(
                {"success": True, "message": "USER GET HIT!"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "PUT":
        """
        Updates a user.
        @Endpoint: /users/:id
        """
        try:
            return Response(
                {"success": True, "message": "USER UPDATE HIT!"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "DELETE":
        """
        Deletes a user.
        @Endpoint: /users/:id
        """
        try:
            user = User.objects.get(ID=id)
            user.delete()
            return Response(
                {"success": True, "message": translationService.translate('user.delete.successful')},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
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
