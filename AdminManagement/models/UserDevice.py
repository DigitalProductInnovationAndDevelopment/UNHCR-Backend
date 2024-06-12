import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from .TimestampAbstractModel import TimestampAbstractModel
from EndUserManagement.models import User

class UserDevice(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    UserID = models.ForeignKey(User, db_column = 'UserID', on_delete = models.CASCADE)
    DeviceID = models.CharField(max_length = 255)
    Brand = models.CharField(max_length = 255, default = "")
    OS = models.CharField(max_length = 20, default = "")
    AppVersion = models.CharField(max_length = 20, default = "")
    NotificationToken = models.CharField(max_length = 255, default = "")
    IsNotificationTokenExpiredn = models.BooleanField(max_length = 255, default = "")

    class Meta:
        db_table = 'UserDevice'