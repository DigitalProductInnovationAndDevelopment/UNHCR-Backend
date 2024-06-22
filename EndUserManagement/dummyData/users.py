import os
import datetime

dummyUsers = [
    {
        "Name": "Ali",
        "Surname": "Mohammed",
        "DateOfBirth": datetime.date(1975, 4, 18),
        "PlaceOfBirth": "Haseke",
        "Gender": "MALE",
        "PhoneNumber": "1234567889",
        "EmailAddress": "mo@hotmail.com",
        "ProvinceOfResidence": "Adana",
        "CountryOfAsylum": "Turkey",
        "Nationality": "Syria",
        "NationalIdNumber": None,
        "CountryOfAsylumRegistrationNumber": "99123456789",
        "UnhcrIndividualId": "385-23C00891",
        "HouseholdPersonCount": 8,
        "ReceiveMessagesFromUnhcr": True,
        "ReceiveNotificationsFromUnhcr": True,
        "ReceiveSurveysFromUnhcr": False,
    },
    {
        "Name": "Eduard",
        "Surname": "Putincev",
        "DateOfBirth": datetime.date(2005, 3, 25),
        "PlaceOfBirth": "Kiev",
        "Gender": "MALE",
        "PhoneNumber": "380633526276",
        "EmailAddress": "eduard@gmail.com",
        "ProvinceOfResidence": "Chisinau",
        "CountryOfAsylum": "Moldova",
        "Nationality": "Ukraine",
        "NationalIdNumber": "12345678-12345",
        "CountryOfAsylumRegistrationNumber": None,
        "UnhcrIndividualId": "XD6-22-12345",
        "HouseholdPersonCount": 3,
        "ReceiveMessagesFromUnhcr": True,
        "ReceiveNotificationsFromUnhcr": True,
        "ReceiveSurveysFromUnhcr": True,
    },
    {
        "Name": "Dilshad",
        "Surname": "Rasheed",
        "DateOfBirth": datetime.date(2002, 8, 21),
        "PlaceOfBirth": "Tehran",
        "Gender": "FEMALE",
        "PhoneNumber": "96407704945860",
        "EmailAddress": "dilshad@whoknows.com",
        "ProvinceOfResidence": "Duhok",
        "CountryOfAsylum": "Iraq",
        "Nationality": "Iran",
        "NationalIdNumber": "1234567890",
        "CountryOfAsylumRegistrationNumber": "DUDOF1234567890",
        "UnhcrIndividualId": "300-19C00210",
        "HouseholdPersonCount": 5,
        "ReceiveMessagesFromUnhcr": False,
        "ReceiveNotificationsFromUnhcr": True,
        "ReceiveSurveysFromUnhcr": False,
    }
]

def getDummyUsers():
    return dummyUsers
