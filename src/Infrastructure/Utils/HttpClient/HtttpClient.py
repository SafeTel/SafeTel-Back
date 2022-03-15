##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## HtttpClient
##

### INFRA
import requests

class HttpClient():
    def __init__(self):
        self.validationCode = 200
        self.header = "text/html; charset=UTF-8"


    def IsUp(self, uri):
        response = requests.get(uri)
        if (response.status_code != self.validationCode):
            return False
        return True


    def Get(self, uri, queries):
        response = requests.get(uri, queries)
        if (response.status_code != self.validationCode
        or response.headers != self.header):
            return None
        return response.json()


    def Post(self, uri, body):
        response = requests.post(uri, body)
        if (response.status_code != self.validationCode
        or response.headers != self.header):
            return None
        return response.json()


    def Delete(self, uri, body):
        response = requests.delete(uri, body)
        if (response.status_code != self.validationCode
        or response.headers != self.header):
            return None
        return response.json()
