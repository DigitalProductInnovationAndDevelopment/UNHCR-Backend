import traceback
import logging
import json

from EndUserManagement.models import User
from EndUserManagement.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.inputValidators import UserCreateValidator

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
            pass

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
        @BodyParam: Name (String, REQUIRED)
        @BodyParam: Surname (String, REQUIRED)
        @BodyParam: DateOfBirth (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: PhoneNumber (String, OPTIONAL)
        @BodyParam: Email (String, REQUIRED)
        @BodyParam: Address (String, OPTIONAL)
        """
        try:
            requestBody = json.loads(request.body)
            paramValidator = UserCreateValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            newUser = User(**validatedData)
            newUser.save()
            return Response(
                {"success": True, "message": translationService.translate('user.create.successful')},
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
