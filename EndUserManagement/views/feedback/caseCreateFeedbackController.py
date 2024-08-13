import json
import traceback
import logging

from EndUserManagement.models import Case, CaseCreateFeedback
from EndUserManagement.serializers.inputValidators import CaseCreateFeedbackCreateValidator
from EndUserManagement.serializers.responseSerializers import CaseCreateFeedbackCreateResponseSerializer

from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["POST"])
def caseCreateFeedbackController(request, id, **kwargs):
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
    
    if request.method == "POST":
        """
        Creates a case feedback.
        @Endpoint: /cases/:id/feedback
        @BodyParam: Rating (Integer, REQUIRED) (Star rating of the case creation experience. It can be values from 1 to 5)
        @BodyParam: Description (String, OPTIONAL) (Text description for the case creation experience)
        """
        try:
            requestBody = json.loads(request.body)
            paramValidator = CaseCreateFeedbackCreateValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            newCaseCreateFeedback = CaseCreateFeedback(Case = case, **validatedData)
            newCaseCreateFeedback.save()
            responseSerializer = CaseCreateFeedbackCreateResponseSerializer(newCaseCreateFeedback)

            case.IsFeedbackNeeded = False

            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_201_CREATED,
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
