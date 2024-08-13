import requests

from django.test import TestCase
from EndUserManagement.models import Case
from EndUserManagement.dummyData import getDummyCases, getDummyUsers


class UsersTestCase(TestCase):
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

    def test_get_user(self):
        getUserUrl = self.baseServerUrl + "/users"
        getUserHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }
        response = requests.get(getUserUrl, headers = getUserHeaders)
        responseData = None
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            responseData = response.json()      
        else:
            raise Exception("Get user request failed.")
        # Check if response is not an empty list
        userFetched = responseData['data']
        self.assertNotEqual(userFetched, [])

        #get Dummy Data
        dummyUsers = getDummyUsers()

        name_to_find = "Eduard"
        userExpected = [user for user in dummyUsers if user["Name"] == name_to_find]
        userObserved = userFetched
    
        # Comparing the expected and observed emails of the cases
        self.assertIsNotNone(userExpected, userObserved)
        self.assertEqual(userExpected["EmailAddress"], userObserved["EmailAddress"])

    def test_user_update(self):
        """Animals that can speak are correctly identified"""
        print("test_user_update")

    def test_user_delete(self):
        """Animals that can speak are correctly identified"""
        print("test_user_delete")
    
    # NO CASE DELETE AND UPDATE FOR THE END USER