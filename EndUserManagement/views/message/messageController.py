import os
import traceback
import logging
import json
import uuid

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.http import JsonResponse
from EndUserManagement.models import User
from EndUserManagement.models import Case
from EndUserManagement.models import Message
from EndUserManagement.models.Media import Media
from EndUserManagement.serializers.responseSerializers.messageListResponseEndUserSerializer import \
    MessageListResponseEndUserSerializer
from EndUserManagement.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.responseSerializers import createCaseListResponseEndUserSerializer
from EndUserManagement.serializers.inputValidators import createCaseListValidator, CaseCreateValidator

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "POST","PUT"])
def messageController(request, **kwargs):

    if request.method == "GET":
        """
              Gets a case.
              @Endpoint: /messages/
              """
        case_id = request.GET.get('Case')
        print(case_id)
        try:
            case_id = request.GET.get('Case')
            print(case_id)
            if not Case.objects.filter(ID=int(case_id)).exists():
                return Response({"success": False, "message": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
            messages = Message.objects.filter(Case=case_id).order_by('CreatedAt')
            print(len(messages))
            serializer = MessageListResponseEndUserSerializer(messages, many=True)
            return Response(
                {"success": True, "message": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Message.DoesNotExist as err:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('message.not.exist')},
                status=status.HTTP_404_NOT_FOUND,
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
             @Endpoint: /messages
             @QueryParam: User (Int, REQUIRED (For the end user), OPTIONAL (For admins))
             (ID of the user whose cases will be fetched)
             @QueryParam: Description (String, OPTIONAL) (Part of the description of the description of the wanted case(s))
             """
        if request.method == "POST":
            # Get params
            user_id = request.POST.get('User')
            case_id = request.POST.get('Case')
            contentFile = request.FILES.get('content_file')
            text_message = request.POST.get('TextMessage')
            userToGet = User.objects.get(ID=user_id)
            caseToGet = Case.objects.get(ID=case_id)

            print(userToGet)
            print(text_message)
            print(caseToGet)




            #newMessage.save()
            # Save the media


            if contentFile is not None:
                hasMedia = True
                print(hasMedia)
                content_file = request.FILES.get('content_file')
                if isinstance(content_file, TemporaryUploadedFile) or isinstance(content_file, InMemoryUploadedFile):
                    # tmp dir
                    tmp_dir = '/tmp'

                    # Check path exists
                    if not os.path.exists(tmp_dir):
                        try:
                            # Create tmp
                            os.makedirs(tmp_dir)
                            print("Created tmp directory:", tmp_dir)
                        except OSError as e:
                            # Dizin oluşturma hatası
                            return JsonResponse({"success": False, "message": "Couldn't create tmp directory"}, status=500)

                    salt = uuid.uuid4().hex
                    original_filename = content_file.name
                    # Get the MIME type of the file
                    file_type = content_file.content_type
                    print("File type:", file_type)
                    base_name, extension = os.path.splitext(original_filename)
                    new_filename = f"{base_name}_{salt}{extension}"  # yeni dosya ismi
                    # Geçici dosyanın tam yolu
                    tmp_file_path = os.path.join(tmp_dir, new_filename)
                    print("Geçici dosya tam yolu:", tmp_file_path)  # Geçici dosyanın tam yolunu yazdır
                    # Geçici dosyayı oluştur
                    with open(tmp_file_path, 'wb') as tmp_file:
                        for chunk in content_file.chunks():
                            tmp_file.write(chunk)
                    new_media = Media(
                        User=userToGet,
                        media_type=file_type,
                        path=tmp_file_path,
                        url = f"http://127.0.0.1:8000/api/media?Name={new_filename}",
                        file_name=new_filename
                    )

                    new_media.save()
                    new_message = Message(
                        User=userToGet,
                        Case=caseToGet,
                        TextMessage=text_message,
                        has_media=hasMedia,
                        Media= new_media
                    )
                    new_message.save()
                    serializer = MessageListResponseEndUserSerializer(new_message)

                    print(serializer.data)
                else:
                    return JsonResponse({"success": False, "message": "Geçersiz dosya"}, status=400)
            else:
                hasMedia = False
                new_message = Message(
                    User=userToGet,
                    Case=caseToGet,
                    TextMessage=text_message,
                    has_media=hasMedia
                )
                new_message.save()
                serializer = MessageListResponseEndUserSerializer(new_message)
                print(hasMedia)
                print(serializer.data)
            # Check parameters
            if not all([user_id, text_message]):
                return JsonResponse({"success": False, "message": "Missing parameters"}, status=400)

            # On Success
            return JsonResponse({"success": True, "message":serializer.data}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Only post requests"}, status=405)