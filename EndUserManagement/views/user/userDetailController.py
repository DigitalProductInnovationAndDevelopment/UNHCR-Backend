import traceback
import logging

from EndUserManagement.models import User
from EndUserManagement.services import (
    PaginationService,
    TranslationService,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from EndUserManagement.serializers.inputValidators import createCaseUpdateValidator
from EndUserManagement.serializers.responseSerializers import createUserFetchResponseSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "PUT", "DELETE"])
def userDetailController(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a user.
        @Endpoint: /users/:id
        """
        try: 
            user = User.objects.get(ID=id)
            responseSerializer = createUserFetchResponseSerializer(user)
            serializedUser = responseSerializer(user).data
            return Response(
                {"success": True, "data": serializedUser},
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
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "PUT":
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
            user_id = request.query_params.get('id')
            requestBody = json.loads(request.body)
            user = User.objects.get(id=user_id)
            paramValidator = UserUpdateValidator(data=requestBody, instance=user)
            isParamsValid = paramValidator.is_valid(raise_exception=False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            for attr, value in validatedData.items():
                setattr(user, attr, value)
            user.save()
            return Response(
                {"success": True, "message": translationService.translate('user.update.successful')},
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
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "DELETE":
        """
        Deletes a user.
        @Endpoint: /users/:id
        """
        try:
            return Response(
                {"success": True, "message": "USER DELETE HIT!"},
                status=status.HTTP_200_OK,
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
