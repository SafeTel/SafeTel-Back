##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetTellows
##

# Network imports

from os import strerror
from flask.globals import request
from flask_restful import Resource
from Routes.Service.Tellows.tellowsConfig import TELLOWS_API_KEY_MD5, TELLOWS_URL, MINIMAL_TELLOW_NOTATION_SCORE
import requests

# Utils import
import re

def validatePhoneNumber(phoneNumber):
    phoneNumberWithoutSpaces = phoneNumber.replace(' ', '')
    regexResult = re.search('^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', phoneNumberWithoutSpaces) ## Regext that match phone numbers: https://regex101.com/r/DsaRfI/1
    if regexResult == None:
        return False
    return True

class GetTellows(Resource):
    def generateValidTellowsJsonRequestForFrance(self):
        return {
            'apikeyMd5': TELLOWS_API_KEY_MD5,
            'json': 1, # response as JSON
        }

    def get(self):
        requestUrlQueryParams = self.generateValidTellowsJsonRequestForFrance()
        phoneNumber = request.args.get('phonenumber')

        if phoneNumber == None:
            return {
                'error': 'bad_request - missing phonenumber'
            }, 400
        if not validatePhoneNumber(phoneNumber):
            return {
                'error': 'bad_request - Wrong phone number format - https://regex101.com/r/LbpovI/1' ## Maybe remove the regex link
            }, 400
        ## Get response with the tellows review of the phone number
        tellowsReviewResponse = requests.get(TELLOWS_URL+ phoneNumber, requestUrlQueryParams)

        if tellowsReviewResponse.status_code != 200:
            return {
                'error': 'Internal Server error - Tellows response failed'
            }, 500
        if tellowsReviewResponse.headers['Content-Type'] == 'text/html; charset=UTF-8':
            return {
                'error': 'unknown phone number'
            }, 404
        jsonTellowsReviewResponse = tellowsReviewResponse.json()

        if not 'tellows' in jsonTellowsReviewResponse:
            return {
                'error': 'unknown phone number'
            }, 404
        if not 'score' in jsonTellowsReviewResponse['tellows']:
            return {
                'error': 'unknown phone number'            
            }, 404
        score = int(jsonTellowsReviewResponse['tellows']['score'])

        if score >= MINIMAL_TELLOW_NOTATION_SCORE:
            return {
                'valid': True
            }, 200
        return {
            'valid': False
        }, 200
