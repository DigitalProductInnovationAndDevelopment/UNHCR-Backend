import uuid

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel

from .Message import Message

# The model for the case media of a case
class MessageMedia(TimestampAbstractModel):
    ID = models.UUIDField(primary_key = True, db_column = 'ID', default = uuid.uuid4, editable = False)
    Message = models.ForeignKey(Message, db_column = 'Message', on_delete = models.CASCADE)
    MediaType = models.TextField()
    MediaName = models.TextField()
    TestField = models.TextField()

    class Meta:
        db_table = 'MessageMedia'