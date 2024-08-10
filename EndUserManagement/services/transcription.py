import os
import whisper
from EndUserManagement.models import MessageMedia, CaseMedia, CaseMediaTranscription, MessageMediaTranscription
from EndUserManagement.services import MediaService

mediaService = MediaService()


class TranscriptionService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.caseMediaStoragePath = "UNHCR_Backend/mediaStorage/case"
        self.coreAppDir = os.getcwd()
        self.model = whisper.load_model("base")

    def speechToTextFromFile(self, media_instance, media_type):
        audio_path = mediaService.getFilePath(media_instance, media_type)

        result = self.model.transcribe(audio_path, fp16=False)
        return result['text'], result['language']


    def transcribeCaseMedia(self, case_media):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(case_media, "case")

            case_media_transcription = CaseMediaTranscription(
                CaseMedia=case_media,
                TranscriptionText=transcription_text,
                Language=detected_language
            )

            case_media_transcription.save()

            return transcription_text
        except CaseMedia.DoesNotExist:
            return None

    def transcribeMessageMedia(self, message_media):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(message_media, "message")

            message_media_transcription = MessageMediaTranscription(
                MessageMedia=message_media,
                TranscriptionText=transcription_text,
                Language=detected_language
            )

            message_media_transcription.save()

            return transcription_text
        except MessageMedia.DoesNotExist:
            return None