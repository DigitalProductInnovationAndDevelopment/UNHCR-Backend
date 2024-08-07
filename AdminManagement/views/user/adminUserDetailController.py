import traceback
import logging
import json

from EndUserManagement.models import User
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from AdminManagement.serializers.inputValidators import AdminUserUpdateValidator
from AdminManagement.serializers.responseSerializers import AdminUserGetResponseSerializer, AdminUserUpdateResponseSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "PATCH", "DELETE"])
def adminUserDetailController(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a user.
        @Endpoint: /users/:id
        """
        try: 
            user = User.objects.get(ID=id)
            responseSerializer = AdminUserGetResponseSerializer(user)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
            )
        
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('user.not.found')},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "PATCH":
        """
        Updates a user.
        @Endpoint: /users/:id
        @BodyParam: Name (String, OPTIONAL)
        @BodyParam: Surname (String, OPTIONAL)
        @BodyParam: DateOfBirth (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: PhoneNumber (String, OPTIONAL)
        @BodyParam: EmailAddress (String, OPTIONAL)
        @BodyParam: Address (String, OPTIONAL)
        """
        try:
            user = User.objects.get(ID=id)
            requestBody = request.body.decode('utf-8')
            bodyParams = json.loads(requestBody)
            bodyParamsValidator = AdminUserUpdateValidator(data = bodyParams)
            isBodyParamsValid = bodyParamsValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isBodyParamsValid:
                return Response(
                    {"success": False, "message": str(bodyParamsValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = bodyParamsValidator.validated_data
            for attr, value in validatedData.items():
                setattr(user, attr, value)
            user.save()
            responseSerializer = AdminUserUpdateResponseSerializer(user)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('user.not.found')},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                {"success": True, "message": translationService.translate("user.delete.successful")},
                status=status.HTTP_200_OK,
            )
        
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate("user.not.exist")},
                status=status.HTTP_404_NOT_FOUND,
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
