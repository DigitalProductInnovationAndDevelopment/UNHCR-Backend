import traceback
import logging
import json

from EndUserManagement.models import Case
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.inputValidators import CaseUpdateValidator
from EndUserManagement.serializers.responseSerializers import CaseGetResponseSerializer, CaseUpdateResponseSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "PATCH", "DELETE"])
def caseDetailController(request, id, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]
    try:
        case = Case.objects.get(ID=id)
        # The case for user trying to operate on a case which does not belong to him/her
        if user.ID != case.User.ID:
            return Response(
                    {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
    except Case.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        """
        Gets a case.
        @Endpoint: /cases/:id
        """
        try:
            responseSerializer = CaseGetResponseSerializer(case)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "PATCH":
        """
        Updates a case.
        @Endpoint: /cases/:id
        @BodyParam: Coverage (String ("INDIVIDUAL" OR "HOUSEHOLD"), OPTIONAL)
        @BodyParam: Description (String, OPTIONAL)
        @BodyParam: CaseTypes (String, REQUIRED, LIST) (IDs of the case types.)
        @BodyParam: PsnTypes (String, OPTIONAL, LIST) (IDs of the case types.)
        """
        try:
            requestBody = request.body.decode('utf-8')
            bodyParams = json.loads(requestBody)
            bodyParamsValidator = CaseUpdateValidator(data = bodyParams)
            isBodyParamsValid = bodyParamsValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isBodyParamsValid:
                return Response(
                    {"success": False, "message": str(bodyParamsValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = bodyParamsValidator.validated_data
            caseUpdateDict = validatedData.copy()
            caseUpdateDict.pop("CaseTypes", None)
            caseUpdateDict.pop("PsnTypes", None)
            for attr, value in caseUpdateDict.items():
                setattr(case, attr, value)
            case.save()
            if "CaseTypes" in validatedData:
                case.CaseTypes.set(validatedData["CaseTypes"])
            if "PsnTypes" in validatedData:
                case.PsnTypes.set(validatedData["PsnTypes"])
            responseSerializer = CaseUpdateResponseSerializer(case)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
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
            case.delete()
            return Response(
                {"success": True, "message": translationService.translate('case.delete.successful')},
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
