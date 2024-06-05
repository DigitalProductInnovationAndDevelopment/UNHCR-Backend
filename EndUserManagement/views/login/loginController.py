import traceback
import logging
import json

from django.contrib.auth import authenticate

from EndUserManagement.models import User
from EndUserManagement.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.inputValidators import LoginValidator

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["POST"])
def loginController(request, **kwargs):

    if request.method == "POST":
        """
        Login endpoint. Checks if the user is authenticated and creates the JWT token and returns it.
        @Endpoint: /login
        @BodyParam: EmailAddress
        @BodyParam: Password
        """
        try:
            requestBody = json.loads(request.body)
            # Taking the param name as 'Password' from the user but in the model, it is 'password'
            paramValidator = LoginValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            validatedData = paramValidator.validated_data
            user = authenticate(username = validatedData["EmailAddress"], password = validatedData["Password"])
            # Authenticated case
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "data": {
                            "refresh_token": str(refresh),
                            "access_token": str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_200_OK,
                )
            # Not authenticated case
            else:
                return Response(
                    {"success": False, "message": translationService.translate('user.not.authenticated')},
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
