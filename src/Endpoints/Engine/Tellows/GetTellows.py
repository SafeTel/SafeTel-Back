##
## SAFETEL PROJECT, 2022
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

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

from Models.Endpoints.Engine.TellowsResponse import TellowsResponse

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
            return BadRequestError("Invalid number"), 400

        Response = TellowsResponse(score >= 5)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return Response.ToDict(), 200
