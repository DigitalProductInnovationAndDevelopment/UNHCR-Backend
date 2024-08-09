import uuid

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel

from .Case import Case

# The model for the case media of a case
class CaseMedia(TimestampAbstractModel):
    ID = models.UUIDField(primary_key = True, db_column = 'ID', default = uuid.uuid4, editable = False)
    Case = models.ForeignKey(Case, db_column = 'Case', on_delete = models.CASCADE)
    MediaType = models.TextField()
    MediaName = models.TextField()

    class Meta:
        db_table = 'CaseMedia'