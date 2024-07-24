import os
import whisper
import numpy as np
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
        result = self.model.transcribe(audio_path, fp16=False)
        return result['text'], result['language']

    def speechToTextFromFile(self, voice_recording):
        # Convert InMemoryUploadedFile to a floating point NumPy array
        audio_fp = self._convert_to_float32(voice_recording)
        # Transcribe using the model
        result = self.model.transcribe(audio_fp, fp16=False)
        return result['text'], result['language']

    def _convert_to_float32(self, voice_recording):
        # Read file content into bytes
        audio_bytes = voice_recording.read()
        # Convert bytes to NumPy array
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
        # Convert to float32 and normalize the audio
        audio_fp = audio_np.astype(np.float32) / np.iinfo(np.int16).max
        return audio_fp

    def transcribeCaseMedia(self, voice_recording, case_media):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(voice_recording)

            case_media_transcription, created = CaseMediaTranscription.objects.get_or_create(
                CaseMedia=case_media,
                defaults={'TranscriptionText': transcription_text, 'Language': detected_language}
            )
            if not created:
                case_media_transcription.TranscriptionText = transcription_text
                case_media_transcription.Language = detected_language
                case_media_transcription.save()

            return transcription_text
        except CaseMedia.DoesNotExist:
            return None

    def transcribeMessageMedia(self, voice_recording, message_media):
        try:
            transcription_text, detected_language = self.speechToTextFromFile(voice_recording)

            message_media_transcription, created = MessageMediaTranscription.objects.get_or_create(
                MessageMedia=message_media,
                defaults={'TranscriptionText': transcription_text, 'Language': detected_language}
            )
            if not created:
                message_media_transcription.TranscriptionText = transcription_text
                message_media_transcription.Language = detected_language
                message_media_transcription.save()

            return transcription_text
        except MessageMedia.DoesNotExist:
            return None