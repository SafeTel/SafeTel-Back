##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Tellows
##

### INFRA
# HttpClient import
from Infrastructure.Utils.HttpClient.HtttpClient import HttpClient

### LOGIC
# regex imports
import re
# Get env var import
import os

# External service tellows
class Tellows():
    def __init__(self):
        self.uri = os.getenv("TELLOWS_BASE_URI") + os.getenv("TELLOWS_URI_NUMBER")
        self.query = {
            'apikeyMd5': os.getenv("TELLOWS_API_KEY_MD5"),
            'json': 1
        }
        self.HTTPClient = HttpClient()


    def GetEvaluation(self, number: str):
        if (not self.__IsValidNumber(number)):
            return None
        return self.HTTPClient.Get(self.uri + number, self.query)["tellows"] # TODO: set a model for tellows FIXME: next sprint


    def __IsValidNumber(self, number: str):
        number = number.replace(' ', '')
        match = re.search('^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', number)
        if (match == None):
            return False
        return True
