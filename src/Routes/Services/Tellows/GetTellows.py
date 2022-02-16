##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## GetTellows
##

### INFRA
# Network imports
from flask.globals import request
from flask_restful import Resource
# Tellows Service
from Infrastructure.Services.Tellows.Tellows import Tellows

class GetTellows(Resource):
    def get(self):
        phoneNumber = request.args.get('phonenumber')
        if request.args["magicNumber"] != "42":
            return {
                'error': 'bad_request'
            }, 400
        if phoneNumber == None:
            return {
                'error': 'bad_request - missing phonenumber'
            }, 400

        tellows = Tellows()
        score = tellows.EvaluateNumber(phoneNumber)

        if score is None:
            return {
                'error': 'not a number OR provider unknonw'
            }, 400

        if score >= 5:
            return {
                'valid': True
            }, 200
        return {
            'valid': False
        }, 200
