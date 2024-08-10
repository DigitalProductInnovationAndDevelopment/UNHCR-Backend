from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from .TimestampAbstractModel import TimestampAbstractModel
from .modelChoices import userGenderChoices, userCountryOfAsylumChoices, userNationalityChoices

# The model for the cases of the end users
class User(TimestampAbstractModel, AbstractUser):
    ID = models.BigAutoField(primary_key = True, db_column = 'ID')
    Name = models.CharField(max_length = 255)
    Surname = models.CharField(max_length = 255)
    DateOfBirth = models.DateTimeField()
    PlaceOfBirth = models.CharField(max_length = 255)
    Gender = models.CharField(max_length = 20, choices = userGenderChoices)
    # TODO: UNHCR asks for an integer phone number but how we will detect the country code?
    # For integers bigger than 2147483647, we get error. That is why converted the phone num to string
    PhoneNumber = models.CharField(max_length = 30)
    # Email is used for authentication
    EmailAddress = models.EmailField(unique = True)
    ProvinceOfResidence = models.CharField(max_length = 255)
    CountryOfAsylum = models.CharField(max_length = 255, choices = userCountryOfAsylumChoices)
    Nationality = models.CharField(max_length = 255, choices = userNationalityChoices)
    # null = True and blank = True also behaves as default = None (NULL)
    NationalIdNumber = models.CharField(max_length = 255, null = True, blank = True)
    CountryOfAsylumRegistrationNumber = models.CharField(max_length = 255, null = True, blank = True)
    UnhcrIndividualId = models.CharField(max_length = 255, null = True, blank = True)
    HouseholdPersonCount = models.IntegerField(null = True, blank = True)
    ReceiveMessagesFromUnhcr = models.BooleanField(default = False)
    ReceiveNotificationsFromUnhcr = models.BooleanField(default = False)
    ReceiveSurveysFromUnhcr = models.BooleanField(default = False)
    # Below are the fields inherited from the AbstractUser model
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'EmailAddress'

    class Meta:
        db_table = 'User'

    def calculateAge(self):
        today = date.today()
        birthDate = self.DateOfBirth
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age