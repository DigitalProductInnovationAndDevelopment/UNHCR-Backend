import os
from io import BytesIO
import mimetypes


from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import connection

from EndUserManagement.models import User, Case, Message, CaseType, PsnType
from EndUserManagement.models.modelChoices import caseTypeChoices, psnTypeChoices
from EndUserManagement.dummyData import getDummyUsers, getDummyCases
from EndUserManagement.services import MediaService, MessageService, CaseService

mediaService = MediaService()
messageService = MessageService()
caseService = CaseService()

# Simulating a file upload. Behaving like the dummy data file is uploaded by the end user
def createInMemoryUploadedFile(filePath):
    # Step 1: Read the file
    with open(filePath, 'rb') as f:
        fileContent = f.read()
    
    # Extract the file name from the path
    fileName = os.path.basename(filePath)
    
    # Determine the MIME type of the file
    contentType, _ = mimetypes.guess_type(filePath)
    if contentType is None:
        contentType = 'application/octet-stream'  # Default MIME type
    
    # Step 2: Create a BytesIO object
    fileStream = BytesIO(fileContent)
    
    # Step 3: Create an InMemoryUploadedFile object
    uploadedFile = InMemoryUploadedFile(
        file = fileStream,                # The file stream
        field_name = 'file',               # Field name associated with the file
        name = fileName,                  # Name of the file
        content_type = contentType,       # MIME type
        size = len(fileContent),          # Size of the file in bytes
        charset = None                     # Optional: charset for text files
    )
    
    return uploadedFile


class Command(BaseCommand):
    help = "Custom command to insert dummy data to DB. (python manage.py createDummyData)"

    def handle(self, *args, **options):
        try:
            dummyUsers = getDummyUsers()
            dummyCases = getDummyCases()
            dummyPwd = "1234567"

            for dummyUserInfo in dummyUsers:
                dummyUser = User(**dummyUserInfo)
                dummyUser.set_password(dummyPwd)
                dummyUser.save()
                print("User inserted")
                dummyCasesOfUser = dummyCases[dummyUserInfo["Name"]] if dummyUserInfo["Name"] in dummyCases else None
                if dummyCasesOfUser:
                    for dummyCaseInfo in dummyCasesOfUser:
                        caseCreateDict = dummyCaseInfo.copy()
                        # Extracting the keys which should not be used for case model instance create
                        keysToExtract = ["CaseTypes", "PsnTypes", "File", "VoiceRecording", "Messages"]
                        for keyToExtract in keysToExtract:
                            caseCreateDict.pop(keyToExtract, None)
                        dummyCase = Case(User = dummyUser, **caseCreateDict)
                        # We first need to save the model for attaching many to many fields
                        dummyCase.save()
                        print("Case inserted")
                        # Attaching the case types
                        caseTypes = dummyCaseInfo["CaseTypes"] if "CaseTypes" in dummyCaseInfo else None
                        if caseTypes:
                            chosenCaseTypes = CaseType.objects.filter(name__in = caseTypes)
                            for chosenCaseType in chosenCaseTypes:
                                dummyCase.CaseTypes.add(chosenCaseType)
                        # Attaching the psn types
                        psnTypes = dummyCaseInfo["PsnTypes"] if "PsnTypes" in dummyCaseInfo else None
                        if psnTypes:
                            chosenPsnTypes = PsnType.objects.filter(name__in = dummyCaseInfo["PsnTypes"])
                            for chosenPsnType in chosenPsnTypes:
                                dummyCase.PsnTypes.add(chosenPsnType)
                        # Calculating and setting the vulnerability score for household cases
                        if dummyCase.Coverage == "HOUSEHOLD":
                            vulnerabilityScore, vulnerabilityCategory = caseService.calcCaseVulnerabilityScore(dummyCase)
                            dummyCase.VulnerabilityScore = vulnerabilityScore
                            dummyCase.VulnerabilityCategory = vulnerabilityCategory
                            dummyCase.save()
                        # Attaching the dummy files
                        filesPaths = dummyCaseInfo["File"] if "File" in dummyCaseInfo else None
                        if filesPaths:
                            for filePath in filesPaths:
                                file = createInMemoryUploadedFile(filePath)
                                fileId = mediaService.saveCaseMedia(file, dummyCase)
                        # Attaching the dummy voice recordings
                        voiceRecordingPaths = dummyCaseInfo["VoiceRecording"] if "VoiceRecording" in dummyCaseInfo else None
                        if voiceRecordingPaths:
                            for voiceRecordingPath in voiceRecordingPaths:
                                voiceRecording = createInMemoryUploadedFile(voiceRecordingPath)
                                fileId = mediaService.saveCaseMedia(voiceRecording, dummyCase)
                        # Creating case messages and their media
                        caseMessages = dummyCaseInfo["Messages"] if "Messages" in dummyCaseInfo else None
                        if caseMessages:
                            for dummyMessageInfo in caseMessages:
                                messageCreateDict = dummyMessageInfo.copy()
                                # Extracting the keys which should not be used for case model instance create
                                keysToExtract = ["File", "VoiceRecording"]
                                for keyToExtract in keysToExtract:
                                    messageCreateDict.pop(keyToExtract, None)
                                messageCreateDict["TextMessage"] = messageService.encryptStringMessage(dummyUser.EmailAddress, messageCreateDict["TextMessage"])
                                dummyMessage = Message(Case = dummyCase, **messageCreateDict)
                                dummyMessage.save()
                                # Attaching the dummy files to the dummy message
                                filesPaths = dummyMessageInfo["File"] if "File" in dummyMessageInfo else None
                                if filesPaths:
                                    for filePath in filesPaths:
                                        file = createInMemoryUploadedFile(filePath)
                                        fileId = mediaService.saveMessageMedia(file, dummyMessage)
                                # Attaching the dummy voice recordings to the dummy message
                                voiceRecordingPaths = dummyMessageInfo["VoiceRecording"] if "VoiceRecording" in dummyMessageInfo else None
                                if voiceRecordingPaths:
                                    for voiceRecordingPath in voiceRecordingPaths:
                                        voiceRecording = createInMemoryUploadedFile(voiceRecordingPath)
                                        fileId = mediaService.saveMessageMedia(voiceRecording, dummyMessage)
        except Exception as e:
            print(str(e))
