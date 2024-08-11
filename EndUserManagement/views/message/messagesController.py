import os
import traceback
import logging
import uuid

from rest_framework.response import Response

from EndUserManagement.models import Case, Message
from EndUserManagement.serializers.inputValidators import MessageCreateValidator
from EndUserManagement.serializers.responseSerializers import MessageListResponseSerializer, MessageCreateResponseSerializer
from EndUserManagement.services import MediaService, TranscriptionService, MessageService

from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()
mediaService = MediaService()
transcriptionService = TranscriptionService()
messageService = MessageService()

# Create your views here.
@api_view(["GET", "POST"])
def messagesController(request, id, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]
    try:
        case = Case.objects.get(ID = id)
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
        Gets messages of a case.
        @Endpoint: /cases/:id/messages
        @PathParam: id (ID of the case which the message is related to)
        @QueryParam: page (page parameter for the pagination. Giving it as '2' fetches the second page of the results)
        """
        try:
            # Querying and ordering the messages from the newest to oldest
            messages = Message.objects.filter(Case = case).order_by('-CreatedAt')
            responseSerializer = MessageListResponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(messages, request, responseSerializer,
                                                                                    int(os.environ.get('MESSAGE_PAGINATION_COUNT', '25')))
            #set 0 unReadMessages count for the case from user perspectice
            case.UnreadMessageCount = 0
            case.save()

            return Response({'success': True,
                             'current_page': pageNumber,
                             'page_count': pageCount,
                             'data': data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "POST":
        """
        Creates a message.
        @Endpoint: /cases/:id/messages
        @PathParam: id (ID of the case which the message is related to)
        @BodyParam: TextMessage (String, OPTIONAL) (It can be a file(s) only message)
        @BodyParam: File (File, OPTIONAL) (The file attached to the message. A message should have either a text message or a file or both)
        @BodyParam: VoiceRecording (File, OPTIONAL) (The voice recording attached to the message)
        """
        try:
            paramDict = {
                "TextMessage": request.POST.get("TextMessage", None),
                "File": request.FILES.getlist('File'),
                "VoiceRecording": request.FILES.getlist('VoiceRecording')
            }
            paramValidator = MessageCreateValidator(data = paramDict)
            isParamsValid = paramValidator.is_valid(raise_exception=False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            # Returns empty list if there are no files submitted under the key 'File'
            filesList = validatedData["File"]
            voiceRecordingsList = validatedData["VoiceRecording"]
            messageHasMedia = False
            if filesList or voiceRecordingsList:
                messageHasMedia = True
            # Encrypt the text message before saving it to the DB
            validatedData["TextMessage"] = messageService.encryptStringMessage(user.EmailAddress, validatedData["TextMessage"])
            newMessage = Message(Case = case,
                                 TextMessage = validatedData["TextMessage"],
                                 HasMedia = messageHasMedia,
                                 SenderRole = "User")
            newMessage.save()
            savedFileIds = []
            savedVoiceRecordingIds = []
            if filesList:
                for file in filesList:
                    fileId, messageMediaObj = mediaService.saveMessageMedia(file, newMessage)
                    savedFileIds.append(fileId)
            if voiceRecordingsList:
                for voiceRecording in voiceRecordingsList:
                    voiceRecordingId, newMediaObj = mediaService.saveMessageMedia(voiceRecording, newMessage)
                    transcriptionService.transcribeMessageMedia(newMediaObj, newMessage)
                    savedVoiceRecordingIds.append(voiceRecordingId)  
            responseSerializer = MessageCreateResponseSerializer(newMessage)
            responseDict = responseSerializer.data.copy()
            responseDict['Files'] = savedFileIds
            responseDict['VoiceRecordings'] = savedVoiceRecordingIds
            
            return Response({'success': True,
                             'data': responseDict},
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