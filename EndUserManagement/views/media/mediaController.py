import os
import traceback
import logging
import json
import uuid

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.http import JsonResponse, FileResponse
from EndUserManagement.models import User
from EndUserManagement.models import Case
from EndUserManagement.models import Message
from EndUserManagement.models.Media import Media
from EndUserManagement.serializers.responseSerializers.messageListResponseEndUserSerializer import \
    MessageListResponseEndUserSerializer, MediaSerializer
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
@api_view(["GET","DELETE"])
def mediaController(request, **kwargs):

    if request.method == "GET":
        """
              Gets a media.
              @Endpoint: /media/
              """
        media_name = request.GET.get('Name')
        print(media_name)
        try:
            media_name = request.GET.get('Name')
            print(media_name)
            if not Media.objects.filter(file_name=media_name).exists():
                return Response({"success": False, "message": "Media not found"}, status=status.HTTP_404_NOT_FOUND)
            mediaFileObject = Media.objects.get(file_name=media_name)
            print(mediaFileObject)
            print(mediaFileObject.path)
            serializer = MediaSerializer(mediaFileObject)

            # Check if the file exists at the specified path
            if not os.path.exists(mediaFileObject.path):
                return Response({"success": False, "message": "File not found on server"},
                                status=status.HTTP_404_NOT_FOUND)
             # Open the file and create a FileResponse
            response = FileResponse(open(mediaFileObject.path, 'rb'), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{mediaFileObject.file_name}"'

            return response

        except Media.DoesNotExist:
            logger.error(traceback.format_exc())
            return Response({"success": False, "message": "Media does not exist"}, status=status.HTTP_404_NOT_FOUND)
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
    elif request.method == "DELETE":
        """
              Delete a media.
              @Endpoint: /media/
              """
        media_name = request.GET.get('Name')
        print(media_name)
        try:
            media_name = request.GET.get('Name')
            print(media_name)
            if not Media.objects.filter(file_name=media_name).exists():
                return Response({"success": False, "message": "Media not found"},
                                status=status.HTTP_404_NOT_FOUND)
            mediaFileObject = Media.objects.get(file_name=media_name)
            mediaFileObject.delete()

            return Response(
                    {"success": True, "message": "MEDIA DELETE HIT!"},
                    status=status.HTTP_200_OK,
                )

        except Media.DoesNotExist:
            logger.error(traceback.format_exc())
            return Response({"success": False, "message": "Media does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
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

