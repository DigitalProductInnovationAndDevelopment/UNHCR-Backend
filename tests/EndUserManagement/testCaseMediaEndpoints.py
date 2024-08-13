import requests
from django.test import TestCase
from EndUserManagement.models import Case, CaseMedia
from EndUserManagement.services import MediaService
import uuid

class CaseMediaDetailTestCase(TestCase):
    def setUp(self):
        self.baseServerUrl = "http://localhost:8000/api"
        self.dummyUserEmail = "eduard@gmail.com"
        self.dummyUserPwd = "1234567"

        self.mediaService = MediaService()

        payload = {
            "EmailAddress": self.dummyUserEmail,
            "Password": self.dummyUserPwd
        }

        loginUrl = self.baseServerUrl + "/login"
        response = requests.post(loginUrl, json=payload)

        if response.status_code == 200:
            responseData = response.json()
            accessToken = responseData.get('data', {}).get('access_token')
            if accessToken:
                self.dummyUserAccessToken = accessToken
            else:
                raise Exception("No access token in the login response. Check out the test set up method.")
        else:
            raise Exception("Login request failed. Check out the test set up method.")

    def test_get_case_media(self):
        caseGetUrl = f"{self.baseServerUrl}/cases/{1}"
        caseGetHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        response = requests.get(caseGetUrl, headers=caseGetHeaders)

        case_id = 0
        media_id = 0

        if response.status_code == 200:
            responseData = response.json()
            caseRetrieved = responseData.get('data', {})
            case_id = caseRetrieved.ID
            media_id = caseRetrieved.Files[0]

        print(case_id)
        print(media_id)

        
        mediaDetailUrl = f"{self.baseServerUrl}/cases/{case_id}/case-media/{media_id}"
        mediaDetailHeaders = {
            'Authorization': f'Bearer {self.dummyUserAccessToken}'
        }

        response = requests.get(mediaDetailUrl, headers=mediaDetailHeaders)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            self.assertEqual(content_type, "image/jpeg")
        elif response.status_code == 404:
            raise Exception(f"Case or media not found. Response: {response.text}")
        else:
            raise Exception(f"Request failed with status code {response.status_code} and response: {response.text}")
