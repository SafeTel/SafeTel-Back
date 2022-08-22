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
# Error Manager Factory import
from Models.Endpoints.Errors.ErrorManager import ErrorManager
### MODELS
# Model Request & Response import
from Models.Endpoints.Box.Link.ClaimBox.ClaimBoxRequest import ClaimBoxRequest
from Models.Endpoints.Box.Link.ClaimBox.ClaimBoxResponse import ClaimBoxResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/box/link/claim-box
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
class ClaimBox(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Box/Link/Swagger-ClaimBox.yml")
    def post(self):
        Request = ClaimBoxRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User == None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        result = User.Box.ClaimBox(Request.boxid)
        if (type(result) is str):
            return self.__ErrorManager.BadRequestError(result).ToDict(), 400

        Response = ClaimBoxResponse(
            True
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
