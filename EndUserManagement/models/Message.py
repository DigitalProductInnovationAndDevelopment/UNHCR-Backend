from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .Case import Case
from .User import User
from .Media import Media

# The model for the cases of the end users
class Message(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    Case = models.ForeignKey(Case, db_column = 'Case', on_delete = models.CASCADE)
    User = models.ForeignKey(User, db_column = 'User', on_delete = models.CASCADE)
    TextMessage = models.TextField()
    has_media = models.BooleanField(default=False)  # Assuming default is False
    Media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    SenderRole = models.CharField(max_length=20, choices=[
        ("User", "User"),
        ("Supporter", "Case Supporter")
    ])

    class Meta:
        db_table = 'Message'
