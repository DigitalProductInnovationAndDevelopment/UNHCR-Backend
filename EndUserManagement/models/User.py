from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel

# The model for the cases of the end users
class User(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    Name = models.CharField(max_length = 255)
    Surname = models.CharField(max_length = 255)
    DateOfBirth = models.DateTimeField()
    # We can validate the phone number later with regex
    PhoneNumber = models.CharField(max_length = 20, default = "")
    Email = models.EmailField(default = "")
    Address = models.CharField(max_length = 255)

    class Meta:
        db_table = 'User'