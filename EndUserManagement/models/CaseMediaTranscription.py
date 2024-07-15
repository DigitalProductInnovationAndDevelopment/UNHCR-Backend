import uuid

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .CaseMedia import CaseMedia

# The model for the transcriptions of case media
class CaseMediaTranscription(TimestampAbstractModel):
    ID = models.UUIDField(primary_key=True, db_column='ID', default=uuid.uuid4, editable=False)
    CaseMedia = models.OneToOneField(CaseMedia, db_column='CaseMedia', on_delete=models.CASCADE)
    TranscriptionText = models.TextField()

    class Meta:
        db_table = 'CaseMediaTranscription'