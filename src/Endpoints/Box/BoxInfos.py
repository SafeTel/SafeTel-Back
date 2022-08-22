##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetBoxInfos
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
from Models.Endpoints.Box.BoxInfos.BoxInfosRequest import BoxInfosRequest
from Models.Endpoints.Box.BoxInfos.BoxInfosResponse import BoxInfosResponse

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert


### SWAGGER
# flasgger import
from flasgger.utils import swag_from

###
# Request:
# GET: localhost:2407/box/box-infos?token=
###
# Response:
# {
#    "Boxes": [
#        {
#            "boxid": "1234567890",
#            "activity": true,
#            "severity": "normal"
#        },
#        {
#            "boxid": "2345678901",
#            "activity": false,
#            "severity": "low"
#        }
#    ]
# }
###


# Route to get infos of box
class BoxInfos(Resource):
    def __init__(self):
        self.__ErrorManager = ErrorManager()
        self.__JwtConv = JWTConvert()
        self.__UserFactory = UserFactory()


    @swag_from("../../../../swagger/Box/Swagger-BoxInfos.yml")
    def get(self):
        Request = BoxInfosRequest(request.args.to_dict())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__ErrorManager.BadRequestError(requestErrors).ToDict(), 400

        JwtInfos = self.__JwtConv.Deserialize(Request.token)
        if (JwtInfos is None):
            return self.__ErrorManager.BadRequestError("Bad Token").ToDict(), 401

        User = self.__UserFactory.LoadUser(JwtInfos.guid)
        if (User is None):
            return self.__ErrorManager.ForbiddenAccessError().ToDict(), 403

        Response = BoxInfosResponse(
            User.Box.PullBoxes().Boxes
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__ErrorManager.InternalLogicError().ToDict(), 500
        return Response.ToDict(), 200

