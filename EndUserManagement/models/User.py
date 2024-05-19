import datetime

from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel

# The model for the cases of the end users
class User(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    Name = models.CharField(max_length = 255)
    Surname = models.CharField(max_length = 255)
    # DateOfBirth is not required. We want to simplify the registering as much as we can
    DateOfBirth = models.DateTimeField(default = None, blank = True, null = True)
    # Phone number is not required. Some end users may not have a phone number.
    # We can validate the phone number later with regex
    PhoneNumber = models.CharField(max_length = 20, default = "")
    # Email is required for authentication
    Email = models.EmailField()
    # Address is not required
    Address = models.CharField(max_length = 255, default = "")
    # TODO: Maybe we can add a country field in addition to the address (For module filtering)

    class Meta:
        db_table = 'User'