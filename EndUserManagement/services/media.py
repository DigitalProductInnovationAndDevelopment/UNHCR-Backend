import os
import uuid

from django.http import FileResponse
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile

from EndUserManagement.models import MessageMedia, CaseMedia
from EndUserManagement.exceptions import customMessageMediaException, customCaseMediaException
from UNHCR_Backend.services import TranslationService

translationService = TranslationService()

class MediaService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.caseMediaStoragePath = "UNHCR_Backend/mediaStorage/case"
        self.coreAppDir = os.getcwd()

    # SAVE METHODS
    def saveMessageMedia(self, file, message):
        return self.saveMedia(file, MessageMedia, message, 'message')
        
    def saveCaseMedia(self, file, case):
        return self.saveMedia(file, CaseMedia, case, 'case')
        
    def saveMedia(self, file, mediaObjClass, parentObj, mediaType = 'case'):
        fileUuid = uuid.uuid4()
        fileUuidHex = fileUuid.hex
        fileName = file.name
        fileType = file.content_type
        mediaObjCreateDict = {
            "ID": fileUuid,
            "MediaType": fileType,
            "MediaName": fileName
        }
        if mediaType == 'case':
            mediaStoragePath = self.caseMediaStoragePath
            mediaObjCreateDict["Case"] = parentObj
        else:
            mediaStoragePath = self.messageMediaStoragePath
            mediaObjCreateDict["Message"] = parentObj
        # Saving the file to the storage (For now, local storage)
        self.saveMediaFileToStorage(file, mediaStoragePath, file.name, fileUuidHex)
        newMediaObj = mediaObjClass(**mediaObjCreateDict)
        newMediaObj.save()
        return newMediaObj.ID.hex, newMediaObj
        
    def saveMediaFileToStorage(self, file, mediaStoragePath, fileName, uuid):
        saveDirectory = os.path.join(self.coreAppDir, mediaStoragePath, uuid)
        os.makedirs(saveDirectory, exist_ok=True)
        filePath = os.path.join(saveDirectory, fileName)
        with open(filePath, 'wb') as fileHandler:
            for chunk in file.chunks():
                fileHandler.write(chunk)

    # GET METHODS
    def getMessageMediaFileAsFileResponse(self, messageMedia):
        return self.getMediaFileAsFileResponse(messageMedia, 'message', customMessageMediaException)
    
    def getCaseMediaFileAsFileResponse(self, caseMedia):
        return self.getMediaFileAsFileResponse(caseMedia, 'case', customCaseMediaException)
    
    def getMediaFileAsFileResponse(self, mediaInstance, mediaType = 'case', exceptionClass = customCaseMediaException):
        folderName = mediaInstance.ID.hex
        fileName = mediaInstance.MediaName
        if mediaType == 'case':
            mediaStoragePath = self.caseMediaStoragePath
        else:
            mediaStoragePath = self.messageMediaStoragePath
        fileDirectory = os.path.join(self.coreAppDir, mediaStoragePath, folderName, fileName)
        if not os.path.exists(fileDirectory):
            raise customCaseMediaException(translationService.translate(f'{mediaType}.media.not.exist'))
        # content_type is octet-stream for now, but we can change it with messageMedia.MediaType
        response = FileResponse(open(fileDirectory, 'rb'), content_type = 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        return response