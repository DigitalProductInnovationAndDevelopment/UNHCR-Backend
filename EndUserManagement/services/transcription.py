import os
import whisper
import tempfile

from EndUserManagement.models import MessageMedia, CaseMedia, CaseMediaTranscription, MessageMediaTranscription
from EndUserManagement.services import MediaService

mediaService = MediaService()


class TranscriptionService:
    def __init__(self):
        self.messageMediaStoragePath = "UNHCR_Backend/mediaStorage/message"
        self.caseMediaStoragePath = "UNHCR_Backend/mediaStorage/case"
        self.coreAppDir = os.getcwd()
        self.model = whisper.load_model("base")

    def speechToTextFromFile(self, media_instance, media_type, object):
        decrypted_audio = mediaService.getDecryptedMedia(media_instance, media_type, object)

        # Create a temporary file with the .mp3 extension
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            temp_audio_file.write(decrypted_audio)
            temp_audio_file_path = temp_audio_file.name

        try:
            # Load and transcribe the MP3 file using Whisper
            audio = whisper.load_audio(temp_audio_file_path)
            result = self.model.transcribe(audio, fp16=False)
            return result['text'], result['language']
        finally:
            # Ensure the temporary file is deleted after processing
            os.remove(temp_audio_file_path)

    def transcribeCaseMedia(self, case_media, case):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(case_media, "case", case)

            case_media_transcription = CaseMediaTranscription(
                CaseMedia=case_media,
                TranscriptionText=transcription_text,
                Language=detected_language
            )

            case_media_transcription.save()

            return transcription_text
        except CaseMedia.DoesNotExist:
            return None

    def transcribeMessageMedia(self, message_media, message):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(message_media, "message", message)

            message_media_transcription = MessageMediaTranscription(
                MessageMedia=message_media,
                TranscriptionText=transcription_text,
                Language=detected_language
            )

            message_media_transcription.save()

            return transcription_text
        except MessageMedia.DoesNotExist:
            return None