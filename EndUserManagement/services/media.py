import os
import uuid

from django.http import FileResponse
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile

from EndUserManagement.models import MessageMedia
from EndUserManagement.exceptions import customMessageMediaException
from UNHCR_Backend.services import TranslationService

translationService = TranslationService()

class MediaService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.coreAppDir = os.getcwd()

    def saveMessageMedia(self, file, message):
        if isinstance(file, TemporaryUploadedFile) or isinstance(file, InMemoryUploadedFile):
            # tmp dir
            fileUuid = uuid.uuid4()
            fileUuidHex = fileUuid.hex
            fileName = file.name
            fileType = file.content_type
            # Saving the file to the storage (For now, local storage)
            self.saveMessageMediaFileToStorage(file, file.name, fileUuidHex)
            newMessageMedia = MessageMedia(
                ID = fileUuid,
                Message = message,
                MediaType = fileType,
                MediaName = fileName
            )
            newMessageMedia.save()
            return newMessageMedia.ID

    def saveMessageMediaFileToStorage(self, file, fileName, uuid):
        saveDirectory = os.path.join(self.coreAppDir, self.messageMediaStoragePath, uuid)
        os.makedirs(saveDirectory, exist_ok=True)
        filePath = os.path.join(saveDirectory, fileName)
        with open(filePath, 'wb') as fileHandler:
            for chunk in file.chunks():
                fileHandler.write(chunk)

    def getMessageMediaFileAsFileResponse(self, messageMedia):
        folderName = messageMedia.ID.hex
        fileName = messageMedia.MediaName
        fileDirectory = os.path.join(self.coreAppDir, self.messageMediaStoragePath, folderName, fileName)
        if not os.path.exists(fileDirectory):
            raise customMessageMediaException(translationService.translate('message.media.not.exist'))
        # content_type is octet-stream for now, but we can change it with messageMedia.MediaType
        response = FileResponse(open(fileDirectory, 'rb'), content_type = 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        return response