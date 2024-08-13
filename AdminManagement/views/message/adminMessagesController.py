import os
import traceback
import logging
import uuid

from rest_framework.response import Response

from EndUserManagement.models import User, Case, Message
from AdminManagement.serializers.inputValidators import AdminMessageCreateValidator
from AdminManagement.serializers.responseSerializers import AdminMessageCreateResponseSerializer, AdminMessageListResponseSerializer
from EndUserManagement.services import MediaService, MessageService

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
messageService = MessageService()

# Create your views here.
@api_view(["GET", "POST"])
def adminMessagesController(request, id, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    #user = kwargs["loggedUser"]
    try:
        case = Case.objects.get(ID = id)
        # The case for user trying to operate on a case which does not belong to him/her

    except Case.DoesNotExist as err:
        logger.error(traceback.format_exc())
        return Response(
            {"success": False, "message": translationService.translate('case.not.exist')},
            status=status.HTTP_404_NOT_FOUND,
        )
    #Fetch the app user
    user = User.objects.get(ID = case.User.ID)

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
            responseSerializer = AdminMessageListResponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(messages, request, responseSerializer,
                                                                                    int(os.environ.get('MESSAGE_PAGINATION_COUNT', '25')))
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
            paramValidator = AdminMessageCreateValidator(data = paramDict)
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
                                 SenderRole = "Case Supporter")
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
                    translationService.translateMessageVoiceRecording(voiceRecording, newMessage)
                    savedVoiceRecordingIds.append(voiceRecordingId)  
            responseSerializer = AdminMessageCreateResponseSerializer(newMessage)
            responseDict = responseSerializer.data.copy()
            responseDict['Files'] = savedFileIds
            responseDict['VoiceRecordings'] = savedVoiceRecordingIds

            # increase one unread message count every post request for app user perspective
            case.UnreadMessageCount = case.UnreadMessageCount + 1
            #change case status
            newStatus= "CASE WORKER ASSIGNED"
            case.Status = newStatus
            case.save()


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