##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## HtttpClient
##

### INFRA
import requests

class HttpClient():
    def __init__(self):
        self.NominalCode = 200
        self.NominalHeaders = [
            "text/json; charset=utf-8",
            "text/html; charset=UTF-8"
        ]


    def Ping(self, uri: str):
        response = requests.get(uri)
        import sys
        print("---", file=sys.stderr)
        print(response, file=sys.stderr)
        print("---", file=sys.stderr)
        if (self.__IsValidResponse(response)):
            return False
        return True


    def Get(self, uri: str, queries: dict = {}):
        response = requests.get(uri, queries)
        if (self.__IsValidResponse(response)):
            return None
        return response.json()


    def Post(self, uri: str, body: dict):
        response = requests.post(uri, body)
        if (self.__IsValidResponse(response)):
            return None
        return response.json()


    def Delete(self, uri: str, body: dict):
        response = requests.delete(uri, body)
        if (self.__IsValidResponse(response)):
            return None
        return response.json()


    def __IsValidResponse(self, response: requests.Response):
        if (response.status_code != self.NominalCode):
            return False
        for NominalHeader in self.NominalHeaders:
            if (response.headers == NominalHeader):
                return True
        return False
