import os
import datetime

dummyUsers = [
    {
        "Name": "Sadiq",
        "Surname": "Hashem",
        "DateOfBirth": datetime.date(1980, 12, 25),
        "PhoneNumber": "",
        "Email": "hashem7@hotmail.com",
        "Address": "Baghdat, Iraq"
    },
    {
        "Name": "Latimah",
        "Surname": "Emami",
        "DateOfBirth": datetime.date(1995, 8, 14),
        "PhoneNumber": "",
        "Email": "emamila89@hotmail.com",
        "Address": "Aleppo, Syria"
    },
    {
        "Name": "Mandla",
        "Surname": "Sipho",
        "DateOfBirth": datetime.date(1990, 2, 4),
        "PhoneNumber": "",
        "Email": "sipdla@gmail.com",
        "Address": "Istanbul, Turkey"
    },
    {
        "Name": "Mohammad",
        "Surname": "Faraad",
        "DateOfBirth": datetime.date(1987, 6, 20),
        "PhoneNumber": "",
        "Email": "faraadm41@gmail.com",
        "Address": "Berlin, Germany"
    },
    {
        "Name": "Yousef",
        "Surname": "Awad",
        "DateOfBirth": datetime.date(1984, 9, 18),
        "PhoneNumber": "",
        "Email": "awad23@gmail.com",
        "Address": "Cairo, Egypt"
    }
]

def getDummyUsers():
    return dummyUsers
