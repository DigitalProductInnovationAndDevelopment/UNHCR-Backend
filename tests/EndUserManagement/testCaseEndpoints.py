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

    def tearDown(self):
        # Clean up: Delete all test cases created by the tests
        caseListUrl = self.baseServerUrl + "/cases"
        caseListHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }
        response = requests.get(caseListUrl, headers=caseListHeaders)
        if response.status_code == 200:
            responseData = response.json()
            casesList = responseData.get('data', [])
            for case in casesList:
                case_id = case.get('ID')
                if case_id:
                    deleteUrl = f"{self.baseServerUrl}/cases/{case_id}"
                    requests.delete(deleteUrl, headers=caseListHeaders)

    def test_case_list(self):
        # Create a known number of cases to test the list functionality
        self.create_test_case(description='Case for List Test 1')
        self.create_test_case(description='Case for List Test 2')

        caseListUrl = self.baseServerUrl + "/cases"
        caseListHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }
        response = requests.get(caseListUrl, headers=caseListHeaders)
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
        # Create a case to get
        case_id = self.create_test_case(description='Case for Get Test')

        caseGetUrl = f"{self.baseServerUrl}/cases/{case_id}"
        caseGetHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        response = requests.get(caseGetUrl, headers=caseGetHeaders)

        if response.status_code == 200:
            responseData = response.json()
            caseRetrieved = responseData.get('data', {})

            self.assertIsNotNone(caseRetrieved)
            self.assertEqual(caseRetrieved.get('ID'), case_id)
            self.assertEqual(caseRetrieved.get('Description'), 'Case for Get Test')
        else:
            raise Exception(f"Case retrieval request failed with status code {response.status_code} and response: {response.text}")

    def test_case_delete(self):
        # Create a case to be deleted
        case_id = self.create_test_case(description='Case for Deletion')

        caseDeleteUrl = f"{self.baseServerUrl}/cases/{case_id}"
        caseDeleteHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        response = requests.delete(caseDeleteUrl, headers=caseDeleteHeaders)

        self.assertEqual(response.status_code, 200)

        response = requests.get(caseDeleteUrl, headers=caseDeleteHeaders)

        self.assertEqual(response.status_code, 404)

    def create_test_case(self, description='Test Case'):
        caseCreateUrl = self.baseServerUrl + "/cases"
        caseCreateHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        # Prepare data to send as form-data
        data = {
            'Coverage': 'INDIVIDUAL',
            'Description': description,
            'CaseTypes': ','.join(map(str, [1])),
            'PsnTypes': ','.join(map(str, [1]))
        }

        response = requests.post(caseCreateUrl, headers=caseCreateHeaders, data=data)

        if response.status_code == 201:
            responseData = response.json()
            caseCreated = responseData.get('data', {})
    
            return caseCreated.get('ID')
        else:
            raise Exception(f"Case creation request failed with status code {response.status_code} and response: {response.text}")


    def test_case_update(self):
        case_id = self.create_test_case(description='Original Case Description')

        caseUpdateUrl = f"{self.baseServerUrl}/cases/{case_id}"
        caseUpdateHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}',
            'Content-Type': 'application/json'
        }

        updatedData = {
            'Description': 'Updated Case Description',
        }

        response = requests.patch(caseUpdateUrl, headers=caseUpdateHeaders, json=updatedData)

        if response.status_code == 200:
            responseData = response.json()
            caseUpdated = responseData.get('data', {})


            self.assertIsNotNone(caseUpdated)
            self.assertEqual(caseUpdated.get('Description'), updatedData['Description'])
        else:
            raise Exception(f"Case update request failed with status code {response.status_code} and response: {response.text}")