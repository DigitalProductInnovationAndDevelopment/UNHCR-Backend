import traceback
import logging

from EndUserManagement.models import Message, MessageMedia
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
def messageMediaDetailController(request, messageId, mediaId, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]
    try:
        message = Message.objects.get(ID = messageId)
        case = message.Case
        # The case for user trying to operate on a case which does not belong to him/her
        if user.ID != case.User.ID:
            return Response(
                    {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        messageMedia = MessageMedia.objects.get(ID = mediaId)
    
    except Message.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('message.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    except MessageMedia.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('message.media.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    if request.method == "GET":
        """
        Gets a message media.
        @Endpoint: messages/:messageId/message-media/:mediaId
        """
        try:
            # Fetch the file from storage. Return it.
            response = mediaService.getMessageMediaFileAsFileResponse(messageMedia)
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
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )
