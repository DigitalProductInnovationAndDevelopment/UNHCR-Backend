from django.db import models
from .Case import Case
from .modelChoices import caseFeedbackRatingChoices

class CaseCreateFeedback(models.Model):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    Case = models.ForeignKey(Case, db_column = 'Case', on_delete = models.CASCADE)
    Rating = models.IntegerField(choices = caseFeedbackRatingChoices)
    Description = models.CharField(max_length = 255, default = None)

    class Meta:
        db_table = 'CaseCreateFeedback'