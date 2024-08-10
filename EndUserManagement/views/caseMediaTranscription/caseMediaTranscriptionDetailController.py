import traceback
import logging

from EndUserManagement.models import Case, CaseMedia, CaseMediaTranscription
from EndUserManagement.services import MediaService, TranscriptionService
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

@api_view(["GET", "DELETE"])
def caseMediaTranscriptionDetailController(request, caseId, mediaId, transcriptionId, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]

    try:
        case = Case.objects.get(ID=caseId)
        caseMedia = CaseMedia.objects.get(ID=mediaId)
        caseMediaTranscription = CaseMediaTranscription.objects.get(ID=transcriptionId)

        # Ensure the case media belongs to the user
        if user.ID != case.User.ID:
            return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except Case.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    except CaseMedia.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.media.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )

    except CaseMediaTranscription.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.media.transcription.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        """
        Gets a case media transcription.
        @Endpoint: cases/:caseId/case-media/:mediaId/transcription/:transcriptionId
        """
        try:
            return Response(
                {"success": True, "transcription": caseMediaTranscription.TranscriptionText, "language": caseMediaTranscription.Language},
                status=status.HTTP_200_OK
            )

        except CaseMediaTranscription.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('case.media.transcription.not.exist')},
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
        Deletes a case media transcription.
        @Endpoint: cases/:caseId/case-media/:mediaId/transcription/:transcriptionId
        """
        try:
            caseMediaTranscription.delete()
            return Response(
                {"success": True, "message": translationService.translate('case.media.transcription.deleted')},
                status=status.HTTP_200_OK
            )
        except CaseMediaTranscription.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('case.media.transcription.not.exist')},
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