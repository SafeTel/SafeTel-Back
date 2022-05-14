##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdateActivity
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager

### MODELS
# Model Request & Response import
from Models.Endpoints.Embedded.UpdateActivity.UpdateActivityRequest import UpdateActivityRequest
from Models.Endpoints.Embedded.UpdateActivity.UpdateActivityResponse import UpdateActivityResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert

### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# PATCH: localhost:2407/embedded/update-activity
# {
#     "token": "jwt",
#     "boxid": "1234567890",
#     "activity": true
# }
###
# Response:
# {
#       "updated": true
# }
###


# Route to update the activity of a box
class UpdateActivity(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Box/Swagger-UpdateActivity.yml")
    def patch(self):
        Request = UpdateActivityRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        error = User.Box.UpdateActivity(
            Request.boxid,
            Request.activity
        )

        if (error != None):
            return self.__EndpointErrorManager.CreateForbiddenAccessErrorWithMessage(error), 403

        Response = UpdateActivityResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
