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

from AdminManagement.serializers.responseSerializers import AdminUserDeviceGetResponseSerializer
from AdminManagement.serializers.inputValidators import AdminUserDeviceUpdateValidator

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
            userDevice = UserDevice.objects.get(ID=id)
            responseSerializer = AdminUserDeviceGetResponseSerializer(userDevice)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
            )
        except UserDevice.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('userDevice.not.exist')},
                status=status.HTTP_404_NOT_FOUND,
            )
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
        @BodyParam: DeviceID (String, OPTIONAL)
        @BodyParam: Brand (String, OPTIONAL)
        @BodyParam: OS (String, OPTIONAL)
        @BodyParam: AppVersion (String, OPTIONAL)
        @BodyParam: NotificationToken (String, OPTIONAL)
        @BodyParam: IsNotificationTokenExpired (Boolean, OPTIONAL)
        """
        try:
            userDevice = UserDevice.objects.get(ID=id)
            requestBody = request.body.decode('utf-8')
            bodyParams = json.loads(requestBody)
            bodyParamsValidator = AdminUserDeviceUpdateValidator(data = bodyParams)
            isBodyParamsValid = bodyParamsValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isBodyParamsValid:
                return Response(
                    {"success": False, "message": str(bodyParamsValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = bodyParamsValidator.validated_data
            for attr, value in validatedData.items():
                setattr(userDevice, attr, value)
            userDevice.save()
            return Response(
                {"success": True, "message": translationService.translate('userDevice.update.successful')},
                status=status.HTTP_200_OK,
            )

        except UserDevice.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('userDevice.not.exist')},
                status=status.HTTP_404_NOT_FOUND,
            )

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
            userDevice = UserDevice.objects.get(ID=id)
            userDevice.delete()
            return Response(
                {"success": True, "message": translationService.translate("userDevice.delete.successful")},
                status=status.HTTP_200_OK,
            )
        except UserDevice.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate("userDevice.not.exist")},
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
