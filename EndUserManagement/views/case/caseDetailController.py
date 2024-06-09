import traceback
import logging
import json

from EndUserManagement.models import Case
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.inputValidators import createCaseUpdateValidator

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
def caseDetailController(request, id, **kwargs):

    if request.method == "GET":
        """
        Gets a case.
        @Endpoint: /cases/:id
        """
        try:
            return Response(
                {"success": True, "message": "CASE GET HIT!"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "PUT":
        """
        Updates a case.
        @Endpoint: /cases/:id
        @BodyParam: Description (String, OPTIONAL)
        @BodyParam: User (Int, OPTIONAL) (The new user ID for the case)
        (THIS PARAM CAN ONLY BE USED BY ADMIN USERS)
        @BodyParam: Status (String, OPTIONAL) (The new status for the case)
        (THIS PARAM CAN ONLY BE USED BY ADMIN USERS)
        """
        try:
            # TODO: For end users, before update operation, we need to check if the case belongs to the logged in user 
            caseToUpdate = Case.objects.get(ID = id)
            bodyParamsValidatorPtr = createCaseUpdateValidator()
            requestBody = request.body.decode('utf-8')
            bodyParams = json.loads(requestBody)
            bodyParamsValidator = bodyParamsValidatorPtr(data = bodyParams)
            isBodyParamsValid = bodyParamsValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isBodyParamsValid:
                return Response(
                    {"success": False, "message": str(bodyParamsValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = bodyParamsValidator.validated_data
            for attr, value in validatedData.items():
                setattr(caseToUpdate, attr, value)
            caseToUpdate.save()
            return Response(
                {"success": True, "message": translationService.translate('case.update.successful')},
                status=status.HTTP_200_OK,
            )
        
        except Case.DoesNotExist as err:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('case.not.exist')},
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
        Deletes a case.
        @Endpoint: /cases/:id
        """
        try:
            return Response(
                {"success": True, "message": "CASE DELETE HIT!"},
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
