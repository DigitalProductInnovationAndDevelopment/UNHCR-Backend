import requests

from django.test import TestCase
from EndUserManagement.models import Case
from EndUserManagement.dummyData import getDummyCases

class CasesTestCase(TestCase):
    def setUp(self):
        # The host for the docker 
        self.baseServerUrl = "http://localhost:8000"
        self.dummyUserEmail = "eduard@gmail.com"
        self.dummyUserPwd = "1234567"
        payload = {
            "EmailAddress": self.dummyUserEmail,
            "Password": self.dummyUserPwd
        }
        loginUrl = self.baseServerUrl + "/api/login"
        # Send a POST request to the login endpoint
        response = requests.post(loginUrl, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            responseData = response.json()      
            # Extract the accessToken from the response data
            accessToken = responseData.get('data', {}).get('accessToken')
            if accessToken:
                self.dummyUserAccessToken = accessToken
            else:
                print(response.status_code)
                print(response)
                raise Exception("No access token in the login response. Check out the test set up method.")
        else:
            raise Exception("Login request failed. Check out the test set up method.")

    def test_case_list(self):
        caseListUrl = self.baseServerUrl + "/cases"
        caseListHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }
        response = requests.get(caseListUrl, headers = caseListHeaders)
        responseData = None
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            responseData = response.json()      
        else:
            raise Exception("Case list request failed.")
        # Check if response is not an empty list
        casesList = responseData['data']
        self.assertNotEqual(casesList, [])
        self.assertEqual(len(casesList), 2)
        dummyCases = getDummyCases()
        casesExpected = dummyCases["Eduard"]
        casesObserved = casesList
        descriptionsExpected = [case["Description"] for case in casesExpected]
        descriptionsObserved = [case["Description"] for case in casesObserved]
        # Comparing the expected and observed desriptions of the cases
        self.assertEqual(descriptionsExpected, descriptionsObserved)

    def test_case_create(self):
        """Animals that can speak are correctly identified"""
        print("ROARRR")

    def test_case_get(self):
        """Animals that can speak are correctly identified"""
        print("ROARRR")
    
    # NO CASE DELETE AND UPDATE FOR THE END USER