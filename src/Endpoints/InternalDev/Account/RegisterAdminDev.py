##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## RegisterAdminDev
##


### INFRA
# Flask imports
from flask.globals import request
from flask_restful import Resource
# Endpoint Error Manager import
from Infrastructure.Utils.EndpointErrorManager import EndpointErrorManager
# Casper DB imports
from Infrastructure.Services.MongoDB.Casper.ApiKeys import ApiKeyLogDB
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

### MODELS
# Model Request & Response import
from Models.Endpoints.InternalDev.Account.RegisterAdminDevRequest import RegisterAdminDevRequest
from Models.Endpoints.InternalDev.Account.RegisterAdminDevResponse import RegisterAdminDevResponse
# Model for Role import
from Models.Logic.Shared.Roles import Roles

### LOGC
# JWT converter import
from Logic.Services.JWTConvert.JWTConvert import JWTConvert
# Role import
from Models.Logic.Shared.Roles import Roles
# Password converter import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert
# GUID  creation import
import uuid


###
# Request:
# POST: localhost:2407/internaldev/account/register
# {
# 	"magicnumber": 42,
# 	"apiKey": "",
# 	"role": "admin",
# 	"Registration": {
# 		"username": "Example",
# 		"email": "h@example.c",
# 		"password": "pwd"
# 	}
# }
###
# Response:
# {
# 	"created": true,
# 	"username": "Example",
# 	"token": ""
# }
###


# Route to register admin & dev account from Api Key
class RegisterAdminDev(Resource):
    def __init__(self):
        self.__EndpointErrorManager = EndpointErrorManager()
        self.__JwtConv = JWTConvert()
        self.__ApiKeyLogDb = ApiKeyLogDB()
        self.__UserDB = UserDB()
        self.__BlacklistDB = BlacklistDB()
        self.__WhitelistDB = WhitelistDB()
        self.__HistoryDB = HistoryDB()
        self.__PWDConvert = PWDConvert()

    def post(self):
        Request = RegisterAdminDevRequest(request.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return self.__EndpointErrorManager.CreateBadRequestError(requestErrors), 400

        if (not self.__ApiKeyLogDb.isValidApiKey(Request.apiKey)):
            return self.__EndpointErrorManager.CreateBadRequestError("Invalid ApiKey"), 403

        if (self.__UserDB.exists(Request.Registrattion.email)):
            return self.__EndpointErrorManager.CreateBadRequestError("This email is already linked to an account"), 400

        guid = str(uuid.uuid4())
        role = Roles.StrToEnum(Request.role)

        self.__CreateSuper(guid, Request, role)

        Response = RegisterAdminDevResponse(
            self.__UserDB.existByGUID(guid),
            Request.Registrattion.username,
            self.__JwtConv.Serialize(guid, role)
        )

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return self.__EndpointErrorManager.CreateInternalLogicError(), 500
        return Response.ToDict(), 200


    ### PRIVATE

    def __CreateSuper(self, guid: str, Request: RegisterAdminDevRequest, role :Roles):
        Registration = Request.Registrattion.ToDict()
        Registration["guid"] = guid
        Registration["password"] = self.__PWDConvert.Serialize(Request.Registrattion.password)

        self.__CreateSuperInDB(Registration, role)
        self.__CreateSuperLists(guid)


    def __CreateSuperInDB(self, Infos: dict, role :Roles):
        self.__UserDB.addUser(Infos, role)


    def __CreateSuperLists(self, guid: str):
        self.__BlacklistDB.newBlacklist(guid)
        self.__WhitelistDB.newWhitelist(guid)
        self.__HistoryDB.newHistory(guid)
