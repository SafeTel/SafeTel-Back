##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetTellows
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Tellows Service
from Infrastructure.Services.Tellows.Tellows import Tellows
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Model Request & Response import
from Models.Endpoints.Engine.TellowsRequest import TellowsRequest
from Models.Endpoints.Engine.TellowsResponse import TellowsResponse


###
# Request:
# POST: localhost:2407/engine/tellows
# {
# 	"magicnumber": 42,
# 	"number": "06..."
# }
###
# Response:
# {
# 	"validity": true
# }
###


# Route to get a score to tellows
class GetTellows(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__Tellows = Tellows()


    def post(self):
        Request = TellowsRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        score = self.__Tellows.EvaluateNumber(Request.number)

        if (score == None):
            return self.__EndpointErrorManager.CreateBadRequestError("Invalid number"), 400

        Response = TellowsResponse(score >= 5)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
