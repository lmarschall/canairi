
from django.conf import settings

import requests
import json

# handler for keycloak operations
class KeycloakHandler(object):

    interception_success = False

    # retrieve access token for server client
    @staticmethod
    def getAccessToken():

        if(settings.ACCESS_TOKEN == ""):

            url = f"https://{settings.LOGINSERVER_URL}:{settings.LOGINSERVER_PORT}/auth/realms/{settings.LOGINSERVER_REALM}/protocol/openid-connect/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "grant_type": "client_credentials",
                "client_id": settings.LOGINSERVER_CLIENT_NAME,
                "client_secret": settings.LOGINSERVER_CLIENT_SECRET
            }

            try:

                r = requests.post(url = url, data = data, headers = headers)
                rtext = r.text
                json_string = json.loads(rtext)
                # print(rtext)
                settings.ACCESS_TOKEN = json_string['access_token']

            except:

                pass

    # check access token of user request
    @staticmethod
    def checkUserToken(user_token):

        if(settings.ACCESS_TOKEN != ""):

            url = f"https://{settings.LOGINSERVER_URL}:{settings.LOGINSERVER_PORT}/auth/realms/{settings.LOGINSERVER_REALM}/protocol/openid-connect/token/introspect"       
            bearer = 'Bearer ' + settings.ACCESS_TOKEN

            headers =  {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': bearer
            }

            data = {
                "token": user_token,
                "client_id": settings.LOGINSERVER_CLIENT_NAME,
                "client_secret": settings.LOGINSERVER_CLIENT_SECRET
            }

            try:

                r = requests.post(url = url, data = data, headers = headers)
                rtext = r.text
                json_string = json.loads(rtext)
                print(rtext)

                active = json_string['active']
                print(bool(active))
                print(json_string['authorization']['permissions'][0]['scopes'])
                KeycloakHandler.interception_success = bool(active)

            except:
                KeycloakHandler.interception_success = False

        else:
            KeycloakHandler.getAccessToken()
            if(settings.ACCESS_TOKEN != ""):
                KeycloakHandler.checkUserToken(user_token)
            else:
                KeycloakHandler.interception_success = False