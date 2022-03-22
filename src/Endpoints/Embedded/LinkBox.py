##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## LinkBox
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
from Models.Endpoints.Embedded.LinkBox.LinkBoxRequest import LinkBoxRequest
from Models.Endpoints.Embedded.LinkBox.LinkBoxResponse import LinkBoxResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


###
# Request:
# POST: localhost:2407/embedded/link-box
# {
#     "token": "cutest jwt goes here",
#     "boxid": "boxid"
# }
###
# Response:
# {
# 	  "linked": true
# }
###


# Route to link a box to a user
class LinkBox(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    def post(self):
        Request = LinkBoxRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__EndpointErrorManager.CreateBadRequestError("Bad Token"), 400

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__EndpointErrorManager.CreateForbiddenAccessError(), 403

        result = User.Box.ClaimBox(Request.boxid)
        if (type(result) is str):
            return self.__EndpointErrorManager.CreateBadRequestError(result), 400

        Response = LinkBoxResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200
