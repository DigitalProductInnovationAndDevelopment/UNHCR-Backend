from django.db import models
from .TimestampAbstractModel import TimestampAbstractModel
from .User import User
from .modelChoices import caseStatusChoices, caseCoverageChoices, caseTypeChoices, psnTypeChoices, vulnerabilityCategoryChoices

class PsnType(models.Model):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    name = models.CharField(max_length = 100, unique = True, choices = psnTypeChoices)

    def __str__(self):
        return self.name

class CaseType(models.Model):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    name = models.CharField(max_length = 100, unique = True, choices = caseTypeChoices)

    def __str__(self):
        return self.name

# The model for the cases of the end users
class Case(TimestampAbstractModel):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    User = models.ForeignKey(User, db_column = 'User', on_delete = models.CASCADE)
    Coverage = models.CharField(max_length = 20, choices = caseCoverageChoices)
    Description = models.TextField()
    Status = models.CharField(max_length = 25, choices = caseStatusChoices)
    CaseTypes = models.ManyToManyField(CaseType, related_name='CaseTypes')
    # PsnTypes is not required
    PsnTypes = models.ManyToManyField(PsnType, blank = True, related_name='PsnTypes')
    VulnerabilityScore = models.IntegerField(default = None, null = True)
    VulnerabilityCategory = models.CharField(max_length = 25, choices = vulnerabilityCategoryChoices)
    UnreadMessageCount = models.IntegerField(default = 0, null = True)
    IsFeedbackNeeded = models.BooleanField(default = None, null = True)

    class Meta:
        db_table = 'Case'