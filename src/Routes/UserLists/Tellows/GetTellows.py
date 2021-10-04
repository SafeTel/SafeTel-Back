##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetTellows
##

# Network imports

from flask import request as fquest
from flask.globals import request
from flask_restful import Resource
import requests, config

# Utils import
from Routes.Utils.Request import validateBody

# validate Body for Login route
def GetTellowsBodyValidation(data):
    if not validateBody(
        data,
        ["magicNumber", "number"]):
        return False
    if data["magicNumber"] != 42:
        return False
    return True


class GetTellows(Resource):
    def generateValidTellowsJsonRequestForFrance(self, number):
        return {
            'apikeyMd5': '',
            'country': 'fr',
            'country': 'fr',
            'json': 1, # output format json encoded instead of CSV
            'numberformatinternational': 1, # output all numbers with international codes (e.g. +49342156567)
            'lang': 'fr',
            'mosttagged': 1, # get mosttagged caller for phone number
            'minscore': 1, # only show phone numbers with a tellows score equal or higher than minscore
            'mincomments': 3, # only show phone numbers with count comments equal or higher than mincomments
            'showdeeplink': 1 # NOT PERTINENT - Don't know the effect - # show deeplink to tellows phone number
            # 'showcallertypeid': 1, 
            # 'showcallername': 1
            # 'showprefixname': 1
        }

    def get(self):
        body = fquest.get_json()

        if not GetTellowsBodyValidation(body):
            return {
                'error': 'bad_request'
            }, 400

        body = self.generateValidTellowsJsonRequestForFrance(body['number'])

        response = requests.get(config.TELLOWS_URL, body)

        return {
            "response": response
        }, 200

# https://www.tellows.fr/stats/partnerscoredata?apikeyMd5=399a147c51f6942600fa41412f2678d1&country=fr&json=1&numberformatinternational=1&lang=fr&mosttagged=1&minscore=1&mincomments=3&showdeeplink=1&showcallertypeid=1&showcallername=1&showprefixname=1
