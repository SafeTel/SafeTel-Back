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


class GetTellows(Resource):
    def generateValidTellowsJsonRequestForFrance(self):
        return {
            'apikeyMd5': config.TELLOWS_API_KEY_MD5,
            'json': 1, # response as JSON
        }

    def get(self):
        requestUrlQueryParams = self.generateValidTellowsJsonRequestForFrance()

        phoneNumber = request.args.get('phonenumber')

        if phoneNumber == None:
            return {
                'error': 'bad_request - missing phonenumber'
            }, 400

        response = requests.get(config.TELLOWS_URL+ phoneNumber, requestUrlQueryParams)

        if response.status_code != 200:
            return {
                'error': 'Internal Server error'
            }, 400

        data = response.json()

        if not 'tellows' in data:
            return {
                'error': 'Internal Server error'
            }, 400

        if not 'score' in data['tellows']:
            return {
                'error': 'Internal Server error'            
            }, 400

        score = int(data['tellows']['score'])

        if score >= config.MINIMAL_TELLOW_NOTATION_SCORE:
            return {
                'isValid': True
            }, 200

        return {
            'isValid': False
        }, 200
