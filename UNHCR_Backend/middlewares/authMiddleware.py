import traceback
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed

from UNHCR_Backend.services import TranslationService

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
            "/api/admin/"
        ]
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def __setUserInfoToView(self, loggedUser, token, request, view_kwargs):
        view_kwargs["loggedUser"] = loggedUser
        view_kwargs["loggedUserToken"] = token
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # Check if the request path is excluded from authentication
            if any(request.path.startswith(path) for path in self.paths_to_exclude):
                return None  # Skip authentication for excluded paths

            # authenticate() verifies and decodes the token
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                # Unpacking
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

        except InvalidToken:
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
        
        except AuthenticationFailed:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": translationService.translate('HTTP.auth.failed')},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except Exception:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )