##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Tellows
##

### LOGIC
# regex imports
import re

### INFRA
# HttpClient import
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

import os

class Tellows():
    def __init__(self):
        self.uri = os.getenv("TELLOWS_BASE_URI") + os.getenv("TELLOWS_URI_NUMBER")
        self.query = {
            'apikeyMd5': os.getenv("TELLOWS_API_KEY_MD5"),
            'json': 1
        }
        self.HTTPClient = HttpClient()


    def EvaluateNumber(self, number):
        if (not self.__IsValidNumber(number)):
            return None

        response = self.HTTPClient.Get(self.uri + number, self.query)

        if (not "tellows" in response
        and not "score" in response):
            return None

        return int(response['tellows']['score'])


    def __IsValidNumber(self, number):
        number = number.replace(' ', '')
        match = re.search('^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', number)
        if (match == None):
            return False
        return True
