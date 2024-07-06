from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel

from .User import User


# The model for the cases of the end users
class Media(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    #Case = models.ForeignKey(Case, db_column = 'Case', on_delete = models.CASCADE)
    User = models.ForeignKey(User, db_column = 'User', on_delete = models.CASCADE)
    media_type = models.TextField()
    path = models.TextField()
    url = models.TextField()
    file_name = models.TextField()
    class Meta:
        db_table = 'Media'
