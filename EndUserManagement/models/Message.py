import uuid

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .Case import Case

# The model for the cases of the end users
class Message(TimestampAbstractModel):
    ID = models.UUIDField(primary_key = True, db_column = 'ID', default = uuid.uuid4, editable = False)
    Case = models.ForeignKey(Case, db_column = 'Case', on_delete = models.CASCADE)
    # A message might only have media. It might be without text
    TextMessage = models.TextField(default = None, null = True)
    HasMedia = models.BooleanField(default = False)  # Assuming default is False
    SenderRole = models.CharField(max_length = 20, choices = [
        ("User", "User"),
        ("Case Supporter", "Case Supporter")
    ])

    class Meta:
        db_table = 'Message'