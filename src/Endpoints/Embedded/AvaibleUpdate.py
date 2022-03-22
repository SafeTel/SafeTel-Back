##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## AvaibleUpdate
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Model Request & Response import
from Models.Endpoints.Embedded.AvaibleUpdate.AvaibleUpdateRequest import AvaibleUpdateRequest
from Models.Endpoints.Embedded.AvaibleUpdate.AvaibleUpdateResponse import AvaibleUpdateResponse


###
# Request:
# POST: localhost:2407/internaldev/embedembededded/update
# {
# 	"version": 1.0
# }
###
# Response:
# {
# 	"update": true
# }
###


# Route to know if an update is required for the embedded software
class AvaiableUpdate(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()


    def post(self):
        Request = AvaibleUpdateRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        Response = AvaibleUpdateResponse(Request.version == 1.0)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
