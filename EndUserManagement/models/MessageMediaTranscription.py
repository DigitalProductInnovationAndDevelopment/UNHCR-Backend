import uuid

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .MessageMedia import MessageMedia

# The model for the transcriptions of message media
class MessageMediaTranscription(TimestampAbstractModel):
    ID = models.UUIDField(primary_key=True, db_column='ID', default=uuid.uuid4, editable=False)
    MessageMedia = models.OneToOneField(MessageMedia, db_column='MessageMedia', on_delete=models.SET_NULL, null=True, blank=True)
    TranscriptionText = models.TextField()

    class Meta:
        db_table = 'MessageMediaTranscription'
