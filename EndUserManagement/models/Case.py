from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .User import User

# The model for the cases of the end users
class Case(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    User = models.ForeignKey(User, db_column = 'User', on_delete = models.CASCADE)
    Description = models.TextField()
    Status = models.CharField(max_length = 20, choices = [
        ("OPEN", "Open"),
        ("VIEWED", "Viewed"),
        ("CW ASSIGNED", "Case Worker Assigned"),
        ("ON PROGRESS", "On Progress"),
        ("CASE CLOSED", "Case Closed")
    ])

    class Meta:
        db_table = 'Case'