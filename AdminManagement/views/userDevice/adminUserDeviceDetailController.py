import traceback
import logging
import json

from AdminManagement.models import UserDevice
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
def adminUserDeviceDetailController(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a user device.
        @Endpoint: /user-devices/:id
        """
        try: 
            pass
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "PUT":
        """
        Updates a user device.
        @Endpoint: /users/:ids
        @BodyParam: DeviceID (String)
        @BodyParam: Brand (String, OPTIONAL)
        @BodyParam: OS (String, OPTIONAL)
        @BodyParam: AppVersion (String, OPTIONAL)
        @BodyParam: NotificationToken (String, OPTIONAL)
        @BodyParam: IsNotificationTokenExpiredn (Boolean, OPTIONAL)
        """
        try:
          pass

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "DELETE":
        """
        Deletes a user device.
        @Endpoint: /user-devices/:id
        """
        try:
           pass
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
