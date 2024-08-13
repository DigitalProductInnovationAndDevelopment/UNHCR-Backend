import requests

from django.test import TestCase
from django.core.management import call_command

from EndUserManagement.models import Case
from EndUserManagement.dummyData import getDummyCases

class CasesTestCase(TestCase):
    def setUp(self):
        # Insert dummy data to test DB
        call_command('createDummyData')
        # The host for the docker
        self.baseServerUrl = "http://localhost:8000/api"
        self.dummyUserEmail = "eduard@gmail.com"
        self.dummyUserPwd = "1234567"
        payload = {
            "EmailAddress": self.dummyUserEmail,
            "Password": self.dummyUserPwd
        }
        loginUrl = self.baseServerUrl + "/login"
        # Send a POST request to the login endpoint
        response = requests.post(loginUrl, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            responseData = response.json()   
            # Extract the accessToken from the response data
            accessToken = responseData.get('data', {}).get('access_token')
            if accessToken:
                self.dummyUserAccessToken = accessToken
            else:
                raise Exception("No access token in the login response. Check out the test set up method.")
        else:
            raise Exception("Login request failed. Check out the test set up method.")
        
    def test_message_list(self):
        dummyUserCaseWithMessages = Case.objects.filter(Coverage = "HOUSEHOLD").first()
        # Check if Eduard's household case with messages exist (none() method returns the empty queryset)
        self.assertNotEqual(dummyUserCaseWithMessages, Case.objects.none())
        messageListUrl = f"{self.baseServerUrl}/cases/{dummyUserCaseWithMessages.ID}/messages"
        messageListHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }
        response = requests.get(messageListUrl, headers = messageListHeaders)
        responseData = None
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            responseData = response.json()      
        else:
            raise Exception("Message list request failed.")
        observedMessages = responseData['data']
        # Check if response is not an empty list
        self.assertNotEqual(observedMessages, [])
        dummyCases = getDummyCases()
        dummyUserDummyCases = dummyCases["Eduard"]
        dummyCase = None
        for case in dummyUserDummyCases:
            if case["Coverage"] == "HOUSEHOLD":
                dummyCase = case
        # Check if the correct dummy case is found
        self.assertNotEqual(dummyCase, None)
        expectedMessages = dummyCase["Messages"]
        # Comparing the expected and observed number of messages of the case
        self.assertEqual(len(observedMessages), len(expectedMessages))