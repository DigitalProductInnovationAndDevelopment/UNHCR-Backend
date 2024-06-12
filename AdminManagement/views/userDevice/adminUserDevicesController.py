import os
import traceback
import logging
import json

from AdminManagement.models import UserDevice
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from AdminManagement.serializers.inputValidators import AdminUserDeviceCreateValidator

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
def adminUserDevicesController(request, **kwargs):

    if request.method == "GET":
        """
        Lists all user devices.
        @Endpoint: /user-devices
        """
        try:
           pass
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "POST":
        """
        Creates a user device.
        @Endpoint: /user-devices
        @BodyParam: UserID (String, REQUIRED)
        @BodyParam: DeviceID (String, REQUIRED)
        @BodyParam: Brand (String, OPTIONAL)
        @BodyParam: OS (String, OPTIONAL)
        @BodyParam: AppVersion (String, OPTIONAL)
        @BodyParam: NotificationToken (String, OPTIONAL)
        @BodyParam: IsNotificationTokenExpiredn (Boolean, OPTIONAL)
        """
        try:
            requestBody = json.loads(request.body)
            paramValidator = AdminUserDeviceCreateValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            newUserDevice = UserDevice(**validatedData)
            newUserDevice.save()
            return Response(
                {"success": True, "message": translationService.translate('userDevice.create.successful')},
                status=status.HTTP_201_CREATED,
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
