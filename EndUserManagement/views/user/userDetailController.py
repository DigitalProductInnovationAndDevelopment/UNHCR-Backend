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

from EndUserManagement.serializers.inputValidators import UserUpdateValidator
from EndUserManagement.serializers.responseSerializers import UserUpdateResponseSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "PATCH", "DELETE"])
def userDetailController(request, id, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]
    # The case for end user tring to operate on another user except himself/herself
    # Use admin endpoints for operating on other users
    if not user:
        return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    if request.method == "PATCH":
        """
        Updates a user. It is designed for users to update their own accounts.
        @Endpoint: /users/:id
        @BodyParam: Name (String, OPTIONAL)
        @BodyParam: Surname (String, OPTIONAL)
        @BodyParam: DateOfBirth (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: PlaceOfBirth (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: Gender (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: PhoneNumber (String, OPTIONAL)
        @BodyParam: EmailAddress (String, OPTIONAL)
        @BodyParam: ProvinceOfResidence (String, OPTIONAL)
        @BodyParam: CountryOfAsylum (String, OPTIONAL)
        @BodyParam: Nationality (String, OPTIONAL)
        @BodyParam: NationalIdNumber (String, OPTIONAL)
        @BodyParam: CountryOfAsylumRegistrationNumber (String, OPTIONAL)
        @BodyParam: UnhcrIndividualId (String, OPTIONAL)
        @BodyParam: HouseholdPersonCount (Integer, OPTIONAL)
        @BodyParam: ReceiveMessagesFromUnhcr (Boolean, OPTIONAL)
        @BodyParam: ReceiveNotificationsFromUnhcr (Boolean, OPTIONAL)
        @BodyParam: ReceiveSurveysFromUnhcr (Boolean, OPTIONAL)
        """
        try:
            requestBody = request.body.decode('utf-8')
            bodyParams = json.loads(requestBody)
            bodyParamsValidator = UserUpdateValidator(data = bodyParams)
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
            responseSerializer = UserUpdateResponseSerializer(user)
            return Response(
                {"success": True, "message": translationService.translate('user.update.successful')},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"success": False, "data": responseSerializer.data},
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
        Deletes a user. It is designed for users to delete their own accounts.
        @Endpoint: /users/:id
        """
        try:
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
