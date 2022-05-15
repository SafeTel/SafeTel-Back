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
        Response = self.HTTPClient.Get(self.uri + number, self.query)["tellows"]
        return ""


    def GetFullEvaluation(self, number: str):
        if (not self.__IsValidNumber(number)):
            return None
        return self.HTTPClient.Get(self.uri + number, self.query)["tellows"]


    def __IsValidNumber(self, number: str):
        number = number.replace(' ', '')
        match = re.search('^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', number)
        if (match == None):
            return False
        return True

##
{
	"tellows": {
		"number": "0611111111",
		"normalizedNumber": "06-11111111",
		"score": "7",
		"searches": "819",
		"comments": "2",
		"scoreColor": "#f79a01",
		"scorePath": "https:\/\/www.tellows.de\/images\/score\/score7.png",
		"location": "numéro de téléphone mobile",
		"country": "France",
		"callerTypes": {
			"caller": [
				{
					"name": "Agence de recouvrement",
					"count": "1"
				},
				{
					"name": "Harcèlement téléphonique",
					"count": "1"
				}
			]
		}
	}
}