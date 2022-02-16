##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## Tellows
##

### CONFIG
# creds import
from config import TELLOWS_API_KEY_MD5, TELLOWS_BASE_URI, TELLOWS_URI_NUMBER

### LOGIC
# regex imports
import re

### INFRA
# HttpClient import
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

class Tellows():
    def __init__(self):
        self.apiKey = TELLOWS_API_KEY_MD5
        self.uri = TELLOWS_BASE_URI + TELLOWS_URI_NUMBER
        self.queries = {
            'apikeyMd5': TELLOWS_API_KEY_MD5,
            'json': 1
        }
        self.httpClient = HttpClient()


    def EvaluateNumber(self, number):
        if (not self.__IsValidNumber(number)):
            return None

        response = self.httpClient.Get(self.uri + number, self.queries)

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
