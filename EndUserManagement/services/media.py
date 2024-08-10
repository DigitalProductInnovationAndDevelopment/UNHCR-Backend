import os
import uuid

from django.http import HttpResponse
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile

from EndUserManagement.models import MessageMedia, CaseMedia
from EndUserManagement.exceptions import customMessageMediaException, customCaseMediaException

from UNHCR_Backend.services import TranslationService, EncryptionService

translationService = TranslationService()
encryptionService = EncryptionService()

class MediaService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.caseMediaStoragePath = "UNHCR_Backend/mediaStorage/case"
        self.coreAppDir = os.getcwd()

    # SAVE METHODS
    def saveMessageMedia(self, file, message):
        encryptionUserField = message.Case.User.EmailAddress
        return self.saveMedia(file, MessageMedia, message, 'message', encryptionUserField)
        
    def saveCaseMedia(self, file, case):
        encryptionUserField = case.User.EmailAddress
        return self.saveMedia(file, CaseMedia, case, 'case', encryptionUserField)
        
    def saveMedia(self, file, mediaObjClass, parentObj, mediaType = 'case', encryptionUserField = 'default-user-field'):
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
        self.saveMediaFileToStorage(file, mediaStoragePath, file.name, fileUuidHex, encryptionUserField)
        newMediaObj = mediaObjClass(**mediaObjCreateDict)
        newMediaObj.save()
        return newMediaObj.ID.hex, newMediaObj
        
    def saveMediaFileToStorage(self, file, mediaStoragePath, fileName, uuid, encryptionUserField = 'default-user-field'):
        saveDirectory = os.path.join(self.coreAppDir, mediaStoragePath, uuid)
        os.makedirs(saveDirectory, exist_ok=True)
        filePath = os.path.join(saveDirectory, fileName)
        with open(filePath, 'wb') as fileHandler:
            for chunk in file.chunks():
                # Encrypting the chunk of the file before saving
                encryptedChunk = encryptionService.encryptData(encryptionUserField, chunk)
                fileHandler.write(encryptedChunk)

    # GET METHODS
    def getMessageMediaFileAsFileResponse(self, messageMedia):
        encryptionUserField = messageMedia.Message.Case.User.EmailAddress
        return self.getMediaFileAsFileResponse(messageMedia, 'message', customMessageMediaException, encryptionUserField)
    
    def getCaseMediaFileAsFileResponse(self, caseMedia):
        encryptionUserField = caseMedia.Case.User.EmailAddress
        return self.getMediaFileAsFileResponse(caseMedia, 'case', customCaseMediaException, encryptionUserField)
    
    def getFilePath(self, mediaInstance, mediaType):
        folderName = mediaInstance.ID.hex
        fileName = mediaInstance.MediaName
        if mediaType == 'case':
            mediaStoragePath = self.caseMediaStoragePath
        else:
            mediaStoragePath = self.messageMediaStoragePath
    
        return os.path.join(self.coreAppDir, mediaStoragePath, folderName, fileName)

    def getMediaFileAsFileResponse(self, mediaInstance, mediaType = 'case', exceptionClass = customCaseMediaException, encryptionUserField = 'default-user-field'):
        fileName = mediaInstance.MediaName
        fileDirectory = self.getFilePath(mediaInstance, mediaType)
        if not os.path.exists(fileDirectory):
            raise customCaseMediaException(translationService.translate(f'{mediaType}.media.not.exist'))
        fileData = None
        with open(fileDirectory, 'rb') as file:
            fileData = file.read()
        decryptedFileData = encryptionService.decryptData(encryptionUserField, fileData)
        # content_type is octet-stream for now, but we can change it with messageMedia.MediaType
        response = HttpResponse(decryptedFileData, content_type = 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        return response