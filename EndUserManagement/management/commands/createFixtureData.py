import os
from io import BytesIO
import mimetypes


from django.core.management.base import BaseCommand

from EndUserManagement.models import CaseType, PsnType
from EndUserManagement.models.modelChoices import caseTypeChoices, psnTypeChoices

class Command(BaseCommand):
    help = "Custom command to insert fixture data to DB. (python manage.py createFixtureData)"

    def handle(self, *args, **options):
        try:
            # Creating the PSN and Case types
            if not CaseType.objects.all():
                for caseTypeChoice in caseTypeChoices:
                    newCaseType = CaseType(name = caseTypeChoice[0])
                    newCaseType.save()

            if not PsnType.objects.all():
                for psnTypeChoice in psnTypeChoices:
                    newPsnType = PsnType(name = psnTypeChoice[0])
                    newPsnType.save()
        except Exception as e:
            print(str(e))
