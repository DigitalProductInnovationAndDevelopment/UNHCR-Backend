import logging
import time

from jose import jwt
from jose.utils import base64url_decode
from distutils.util import strtobool

from EndUserManagement.exceptions import customAuthTokenException

# Get an instance of a logger
logger = logging.getLogger(__name__)

# TODO: For each exception about authentication, we need a handle mechanism. We can return a generic auth failed message to user
# and we can save the error logs to DB.
class AuthService:
    def __init__(self):
        pass

    def validateAuthToken(self, authToken, ignoreAudience=False):

        headers = jwt.get_unverified_header(authToken)

        message, encoded_signature = str(authToken).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature

        # print('Signature successfully verified')
        claims = jwt.get_unverified_claims(authToken)

        # additionally we can verify the token expiration
        if time.time() > claims["exp"]:
            raise customAuthTokenException("Token is expired")

        # and the Audience (use claims['client_id'] if verifying an access token)
        if not ignoreAudience and claims.get("aud") != self.appClientID:
            raise customAuthTokenException("Token was not issued for this audience.")

        return claims