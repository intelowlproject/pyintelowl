import logging
import requests
import sys

from .exceptions import IntelOwlInvalidAPITokenException

logger = logging.getLogger(__name__)

DEFAULT_TOKEN_FILE = "api_token.txt"

class APIToken:

    def __refresh_token(self, token):
        data = {
            "refresh": token
        }
        url = self.instance + "/api/auth/refresh-token"
        resp = requests.post(url=url, json=data)
        resp_data = resp.json()
        if resp.status_code == 200:
            # Save new sets of token into token file.
            with open(self.token_file, 'w') as fp:
                fp.write(str(resp_data["refresh"]))

            return resp_data["access"]
        else:
            raise IntelOwlInvalidAPITokenException(resp_data)

    def __get_token(self):
        """
        reads token from file and verifies it.\n
        If token is expired, tries to refresh it.
        if refresh fails, then terminates the program.
        """
        if not hasattr(self, "__api_token"):
            refresh = None
            try:
                # read current refresh-able token
                with open(self.token_file, 'r') as fp:
                    refresh = fp.read()
                # make sure token does exist
                if not refresh:
                    logger.error("No API token specified in file: {}".format(self.token_file))
                    return None
            except FileNotFoundError:
                # No token file exists
                logger.error("No token file exists with given name: {}".format(self.token_file))
                return None

            # refresh given token
            try:
                self.__api_token = self.__refresh_token(refresh)
            except IntelOwlInvalidAPITokenException as e:
                logger.exception(e)
                logger.error("API token is invalid. Please ask the administrator to provide you with a new token")
                return None

        return self.__api_token


    def __str__(self):
        token = self.__get_token()
        if token:
            return token
        else:
            raise IntelOwlInvalidAPITokenException("pyintelowl failed. API token is invalid.")


    def __init__(self, token_file, instance):
        self.token_file = token_file
        self.instance = instance
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
