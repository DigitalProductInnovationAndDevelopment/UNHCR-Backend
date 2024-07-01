import os

from django.core.management.base import BaseCommand
from django.db import connection

from EndUserManagement.models import User, Case, CaseType, PsnType
from EndUserManagement.models.modelChoices import caseTypeChoices, psnTypeChoices
from EndUserManagement.dummyData import getDummyUsers, getDummyCases


class Command(BaseCommand):
    help = "Custom command to insert dummy data to DB. (python manage.py createDummyData)"

    def handle(self, *args, **options):
        try:
            dummyUsers = getDummyUsers()
            dummyCases = getDummyCases()
            dummyPwd = "1234567"

            # Creating the PSN and Case types
            if not CaseType.objects.all():
                for caseTypeChoice in caseTypeChoices:
                    newCaseType = CaseType(name = caseTypeChoice[0])
                    newCaseType.save()

            if not PsnType.objects.all():
                for psnTypeChoice in psnTypeChoices:
                    newPsnType = PsnType(name = psnTypeChoice[0])
                    newPsnType.save()

            for dummyUserInfo in dummyUsers:
                dummyUser = User(**dummyUserInfo)
                dummyUser.set_password(dummyPwd)
                dummyUser.save()
                dummyCasesOfUser = dummyCases[dummyUserInfo["Name"]] if dummyUserInfo["Name"] in dummyCases else None
                if dummyCasesOfUser:
                    for dummyCaseInfo in dummyCasesOfUser:
                        caseCreateDict = dummyCaseInfo.copy()
                        caseCreateDict.pop("CaseTypes", None)
                        caseCreateDict.pop("PsnTypes", None)
                        dummyCase = Case(User = dummyUser, **caseCreateDict)
                        # We first need to save the model for attaching many to many fields
                        dummyCase.save()
                        # Attaching the case types
                        chosenCaseTypes = CaseType.objects.filter(name__in = dummyCaseInfo["CaseTypes"])
                        for chosenCaseType in chosenCaseTypes:
                            dummyCase.CaseTypes.add(chosenCaseType)
                        # Attaching the psn types
                        chosenPsnTypes = PsnType.objects.filter(name__in = dummyCaseInfo["PsnTypes"])
                        for chosenPsnType in chosenPsnTypes:
                            dummyCase.PsnTypes.add(chosenPsnType)
        except Exception as e:
            print(str(e))
