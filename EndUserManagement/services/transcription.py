import os
import whisper
from EndUserManagement.models import MessageMedia, CaseMedia, CaseMediaTranscription, MessageMediaTranscription

class TranscriptionService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.caseMediaStoragePath = "UNHCR_Backend/mediaStorage/case"
        self.coreAppDir = os.getcwd()
        self.model = whisper.load_model("base")

    def speechToText(self, media_path):
        # Load and transcribe the audio file from a path
        audio_path = os.path.join(self.coreAppDir, media_path)
        result = self.model.transcribe(audio_path)
        return result['text']

    def speechToTextFromFile(self, voice_recording):
        # Load and transcribe the audio file from an in-memory file
        result = self.model.transcribe(voice_recording)
        return result['text']

    def transcribeCaseMedia(self, voice_recording, case_media):
        try:
            transcription_text = self.speechToTextFromFile(voice_recording)

            case_media_transcription, created = CaseMediaTranscription.objects.get_or_create(
                CaseMedia=case_media,
                defaults={'TranscriptionText': transcription_text}
            )
            if not created:
                case_media_transcription.TranscriptionText = transcription_text
                case_media_transcription.save()

            return transcription_text
        except CaseMedia.DoesNotExist:
            return None

    def transcribeMessageMedia(self, voice_recording, message_media):
        try:
            transcription_text = self.speechToTextFromFile(voice_recording)

            message_media_transcription, created = MessageMediaTranscription.objects.get_or_create(
                MessageMedia=message_media,
                defaults={'TranscriptionText': transcription_text}
            )
            if not created:
                message_media_transcription.TranscriptionText = transcription_text
                message_media_transcription.save()

            return transcription_text
        except MessageMedia.DoesNotExist:
            return None