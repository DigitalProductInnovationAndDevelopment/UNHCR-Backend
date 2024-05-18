from django.db import models

class TimestampAbstractModel(models.Model):

    CreatedAt = models.DateTimeField(auto_now_add = True)
    UpdatedAt = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True
