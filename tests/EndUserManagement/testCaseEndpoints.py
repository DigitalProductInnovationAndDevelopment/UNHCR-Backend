import requests

from django.test import TestCase
from EndUserManagement.models import Case
from EndUserManagement.dummyData import getDummyCases

class CasesTestCase(TestCase):
    def setUp(self):
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
        caseCreateUrl = self.baseServerUrl + "/cases"
        caseCreateHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        # Prepare data to send as form-data
        data = {
            'Coverage': 'INDIVIDUAL',
            'Description': 'Test Description',
            'CaseTypes': ','.join(map(str, [1])),
            'PsnTypes': ','.join(map(str, [1]))
        }

        # Send the POST request with form-data
        response = requests.post(caseCreateUrl, headers=caseCreateHeaders, data=data)

        if response.status_code == 201:
            responseData = response.json()
            caseCreated = responseData.get('data', {})

            self.assertIsNotNone(caseCreated)
            self.assertEqual(caseCreated.get('Description'), data['Description'])
            self.assertEqual(caseCreated.get('Coverage'), data['Coverage'])
            self.assertEqual(caseCreated.get('PsnTypes'), [1])
            self.assertEqual(caseCreated.get('CaseTypes'), [1])
        else:
            raise Exception(f"Case creation request failed with status code {response.status_code} and response: {response.text}")

    def test_case_get(self):
        caseGetUrl = f"{self.baseServerUrl}/cases/{1}"
        caseGetHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        response = requests.get(caseGetUrl, headers=caseGetHeaders)

        if response.status_code == 200:
            responseData = response.json()
            caseRetrieved = responseData.get('data', {})
            print(caseRetrieved)
            self.assertIsNotNone(caseRetrieved)
            self.assertEqual(caseRetrieved.get('ID'), 1)
            self.assertEqual(caseRetrieved.get('Coverage'), 'HOUSEHOLD')
            self.assertEqual(caseRetrieved.get('Description'), "I arrived to Chisinau on x/x/2024 after our house in Kharkiv was bombarded by the Russian army. My father passed awayint eh hospital and together with my mother and sister we sought refuge in Moldova. We need a place to stay, clothes, food and some cashto survive. My mother is pregnant and needs medical assistance as well. We don't speak Romanian and don't know where to get assistance.")
            self.assertEqual(caseRetrieved.get('CaseTypes'), [1, 4, 6, 11])
            self.assertEqual(caseRetrieved.get('PsnTypes'), [])
        else:
            raise Exception(f"Case retrieval request failed with status code {response.status_code} and response: {response.text}")
    
    # NO CASE DELETE AND UPDATE FOR THE END USER