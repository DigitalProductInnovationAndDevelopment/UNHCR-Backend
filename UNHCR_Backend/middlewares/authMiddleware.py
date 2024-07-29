import traceback
import logging

from EndUserManagement.exceptions import customAuthTokenException

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from UNHCR_Backend.services import (
    TranslationService
)

JWT_authenticator = JWTAuthentication()

translationService = TranslationService()

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths_to_exclude = [
            "/__debug__",
            "/api/login",
            "/api/logout",
            "/api/signup",
        ]
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def __setUserInfoToView(self, loggedUser, token, request, view_kwargs):
        view_kwargs["loggedUser"] = loggedUser
        view_kwargs["loggedUserToken"] = token
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # Checking auth for every endpoint except the singup, login and admin endpoints
            if not request.path in self.paths_to_exclude:
                # authenticate() verifies and decode the token
                # If token is invalid, it raises an exception and returns 401
                response = JWT_authenticator.authenticate(request)
                if response is not None:
                    # unpacking
                    user, token = response
                    return self.__setUserInfoToView(user, token, request, view_kwargs)
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "The provided authorization is not valid. No token is provided in the header or the header is missing.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return None

        except InvalidToken as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": "The provided token is invalid or expired.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        except TokenError as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
