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
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

from Models.Endpoints.Engine.TellowsRequest import TellowsRequest
from Models.Endpoints.Engine.TellowsResponse import TellowsResponse

class GetTellows(Resource):
    def get(self):
        EndptErrorManager = EndpointErrorManager()
        Request = TellowsRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return EndptErrorManager.CreateBadRequestError(requestErrors), 400

        tellows = Tellows()
        score = tellows.EvaluateNumber(Request.number)

        if score is None:
            return EndptErrorManager.CreateBadRequestError("Invalid number"), 400

        Response = TellowsResponse(score >= 5)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return EndptErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
