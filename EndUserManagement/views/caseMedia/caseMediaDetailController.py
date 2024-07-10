import traceback
import logging

from EndUserManagement.models import Case, CaseMedia
from EndUserManagement.services import MediaService
from EndUserManagement.exceptions import customMessageMediaException
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
mediaService = MediaService()

# Create your views here.
@api_view(["GET"])
def caseMediaDetailController(request, caseId, mediaId, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]
    try:
        case = Case.objects.get(ID = caseId)
        # The case for user trying to operate on a case which does not belong to him/her
        if user.ID != case.User.ID:
            return Response(
                    {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        caseMedia = CaseMedia.objects.get(ID = mediaId)
    
    except Case.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    except CaseMedia.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.media.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    if request.method == "GET":
        """
        Gets a message media.
        @Endpoint: cases/:caseId/case-media/:mediaId
        """
        try:
            # Fetch the file from storage. Return it.
            response = mediaService.getCaseMediaFileAsFileResponse(caseMedia)
            return response

        except customMessageMediaException as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_404_NOT_FOUND,
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
