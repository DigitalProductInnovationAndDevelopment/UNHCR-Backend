import traceback
import logging

from EndUserManagement.models import Message, MessageMedia, MessageMediaTranscription
from EndUserManagement.serializers.responseSerializers import MessageMediaTranscriptionGetResponseSerializer
from EndUserManagement.services import MediaService
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
def messageMediaTranscriptionDetailController(request, messageId, mediaId, transcriptionId, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]

    try:
        message = Message.objects.get(ID=messageId)
        messageMedia = MessageMedia.objects.get(ID=mediaId)
        messageMediaTranscription = MessageMediaTranscription.objects.get(ID=transcriptionId)

        # Ensure the message media belongs to the user
        if user.ID != message.User.ID:
            return Response(
                {"success": False, "message": translationService.translate("HTTP.not.authorized")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except Message.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('message.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    except MessageMedia.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('message.media.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )

    except MessageMediaTranscription.DoesNotExist:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('message.media.transcription.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        """
        Gets a message media transcription.
        @Endpoint: messages/:messageId/message-media/:mediaId/transcription/:transcriptionId
        """
        try:
            responseSerializer = MessageMediaTranscriptionGetResponseSerializer(messageMediaTranscription)
            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_200_OK,
            )

        except MessageMediaTranscription.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('message.media.transcription.not.exist')},
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
        Deletes a message media transcription.
        @Endpoint: messages/:messageId/message-media/:mediaId/transcription/:transcriptionId
        """
        try:
            messageMediaTranscription.delete()
            return Response(
                {"success": True, "message": translationService.translate('message.media.transcription.deleted')},
                status=status.HTTP_200_OK
            )
        except MessageMediaTranscription.DoesNotExist:
            return Response(
                {"success": False, "message": translationService.translate('message.media.transcription.not.exist')},
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