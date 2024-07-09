import os
import traceback
import logging
import uuid

from django.http import JsonResponse
from rest_framework.response import Response

from EndUserManagement.models import User, Case, Message
from EndUserManagement.serializers.responseSerializers import MessageListResponseSerializer, MessageCreateResponseSerializer
from EndUserManagement.services import MediaService
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
            return Response({'success': True,
                             'current_page': pageNumber,
                             'page_count': pageCount,
                             'data': data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "POST":
        """
        Creates a message.
        @Endpoint: /cases/:id/messages
        @PathParam: id (ID of the case which the message is related to)
        @BodyParam: TextMessage (String, OPTIONAL) (It can be a file(s) only message)
        @BodyParam: File (File, OPTIONAL) (The file attached to the message. A message should have either a text message or a file or both)
        """
        try:
            textMessage = request.POST.get("TextMessage", None)
            # For now, since we only have 1 parameter, not creating an input validator
            if textMessage and not isinstance(textMessage, str):
                return Response({'success': False,
                                 'message': 'The type of the given text message is invalid or the text message is empty.'},
                    status = status.HTTP_400_BAD_REQUEST,
                )
            # Returns empty list if there are no files submitted under the key 'File'
            filesList = request.FILES.getlist('File')
            messageHasMedia = False
            if filesList:
                messageHasMedia = True
            newMessage = Message(Case = case,
                                 TextMessage = textMessage,
                                 HasMedia = messageHasMedia,
                                 SenderRole = "User")
            newMessage.save()
            savedFileIds = []
            if filesList:
                for file in filesList:
                    fileId = mediaService.saveMessageMedia(file, newMessage)
                    savedFileIds.append(fileId)     
            responseSerializer = MessageCreateResponseSerializer(newMessage)
            responseData = responseSerializer.data.copy()
            responseData['Files'] = savedFileIds
            
            return Response({'success': True,
                             'data': responseData},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status = status.HTTP_400_BAD_REQUEST,
            )
        
    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )