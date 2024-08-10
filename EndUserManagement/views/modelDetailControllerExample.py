import traceback
import logging

from EndUserManagement.models import User
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
@api_view(["GET", "PUT", "DELETE"])
def modelsControllerExample(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a model.
        @Endpoint: /models/:id
        """
        try:
            pass

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "PUT":
        """
        Updates a model.
        @Endpoint: /models/:id
        """
        try:
            pass

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "DELETE":
        """
        Deletes a model.
        @Endpoint: /models/:id
        """
        try:
            pass

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
