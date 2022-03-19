##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UserFactory
##

### INFRA
# Low Level interface for DBs imports
from Infrastructure.Services.MongoDB.Melchior.UserDB import UserDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
from Infrastructure.Services.MongoDB.Balthasar.BoxDB import BoxDB
# User sub class import
from Infrastructure.Factory.UserFactory.User import User
# Roles enum import
from Models.Logic.Shared.Roles import Roles

### LOGIC
# Password converter import
from Logic.Services.PWDConvert.PWDConvert import PWDConvert
# Guid import
import uuid

### MODEL
# Register request model import
from Models.Endpoints.Authentification.RegisterRequest import RegisterRequest
from Models.Infrastructure.Factory.InternalUser import InternalUser

### /!\ WARNING /!\ ###
# This is an HIGH LEVEL for MELCHIOR DB interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Factory that load create delete User(s)
class UserFactory():
    def __init__(self):
        self.__UserDB = UserDB()
        self.__BlackListDB = BlacklistDB()
        self.__WhiteListDB = WhitelistDB()
        self.__HistoryDB = HistoryDB()
        self.__BoxDB = BoxDB()
        self.__PWDConvert = PWDConvert()


    ### PUBLIC

    def IsMailRegitered(self, email: str):
        return self.__UserDB.exists(email)


    def IsUser(self, guid: str):
        return self.__UserDB.existByGUID(guid)


    def CreateUser(self, UserInfos: RegisterRequest):
        guid = str(uuid.uuid4())
        IntUser = InternalUser(
            UserInfos.ToDict(),
            guid,
            self.__PWDConvert.Serialize(UserInfos.password)
        )
        self.__CreateUserInDB(IntUser.ToDict())
        self.__CreateUserLists(guid)
        return User(guid)


    def LoginUser(self, email: str, pwd: str):
        user = self.__UserDB.getUser(email)
        if (user == None):
            return False, "This email is not linked to an account"
        if (not self.__PWDConvert.Compare(pwd, user["password"])):
            return False, "You can not connect with this combination of email and password"
        return True, user["guid"]


    def LoadUser(self, guid: str):
        if (not self.__IsUser(guid)):
            return None
        return User(guid)


    def LoadUserByMail(self, email: str):
        if (not self.__UserDB.exists(email)):
            return None
        guid = self.__UserDB.getUser(email)["guid"]
        return User(guid)


    ### PRIVATE

    def __IsUser(self, guid: str):
        return self.__UserDB.existByGUID(guid)


    def __CreateUserInDB(self, UserInfos: dict):
        self.__UserDB.addUser(UserInfos, Roles.USER)


    def __CreateUserLists(self, guid: str):
        self.__BlackListDB.newBlacklist(guid)
        self.__WhiteListDB.newWhitelist(guid)
        self.__HistoryDB.newHistory(guid)
        self.__BoxDB.newDataBox(guid)
