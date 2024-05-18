import os

from django.core.management.base import BaseCommand
from django.db import connection

from EndUserManagement.models import User, Case
from EndUserManagement.dummyData import getDummyUsers, getDummyCases


class Command(BaseCommand):
    help = "Custom command to insert dummy data to DB. (python manage.py createDummyData)"

    def handle(self, *args, **options):
        try:
            dummyUsers = getDummyUsers()
            dummyCases = getDummyCases()

            for dummyUser in dummyUsers:
                dummyUserModel = User(**dummyUser)
                dummyUserModel.save()
                dummyCasesOfUser = dummyCases[dummyUser["Name"]] if dummyUser["Name"] in dummyCases else None
                if dummyCasesOfUser:
                    for dummyCase in dummyCasesOfUser:
                        dummyCase = Case(User = dummyUserModel, **dummyCase)
                        dummyCase.save()
        except Exception as e:
            print(str(e))
