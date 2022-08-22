##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## LoginBox
##

### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# User Factory import
from Infrastructure.Factory.UserFactory.UserFactory import UserFactory
# Error Manager Factory import
from Models.Endpoints.Errors.Factory.ErrorManagerFactory import ErrorManagerFactory# import low level interface Box
from Infrastructure.Services.MongoDB.Balthasar.BoxDB import BoxDB

### MODELS
# Model Request & Response import
from Models.Endpoints.Embedded.LoginBox.LoginBoxRequest import LoginBoxRequest
from Models.Endpoints.Embedded.LoginBox.LoginBoxResponse import LoginBoxResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvertEmbedded import JWTConvertEmbedded


### SWAGGER
# flasgger import
from flasgger.utils import swag_from


###
# Request:
# POST: localhost:2407/embedded/login-box
# {
#     "boxid": "boxid"
# }
###
# Response:
# {
# 	  "token": "1234567890"
# }
###


# Route to login a box
class LoginBox(Resource):
    def __init__(self):
        self.__ErrorManagerFactory = ErrorManagerFactory()
        self.__JwtConv = JWTConvertEmbedded()
        self.__UserFactory = UserFactory()
        self.__BoxDB = BoxDB()


    @swag_from("../../../../swagger/Embedded/Swagger-LoginBox.yml")
    def post(self):
        Request = LoginBoxRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManagerFactory.BadRequestError(requestErrors).ToDict(), 400

        guid = self.__BoxDB.RSUserByBoxID(Request.boxid)
        if (guid == None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        User = self.__UserFactory.LoadUser(guid)
        if (User == None):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        if (not User.Box.IsClaimedByUser(Request.boxid)):
            return self.__ErrorManagerFactory.ForbiddenAccessError().ToDict(), 403

        User.Box.UpdateBoxIp(Request.boxid, request.remote_addr)

        Response = LoginBoxResponse(
            self.__JwtConv.Serialize(
                guid,
                Request.boxid
            )
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManagerFactory.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200
