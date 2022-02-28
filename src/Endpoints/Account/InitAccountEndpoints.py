##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitAccountEndpoints
##

### INFRA
# Infos endpoint imports
from Endpoints.Account.Infos.GetInfos import GetInfos
from Endpoints.Account.Infos.UpdateEmail import UpdateEmail
from Endpoints.Account.Infos.UpdatePersonalInfos import UpdatePersonalInfos
# Lists endpoints imports
from Endpoints.Account.Lists.Greylist import GreyList
from Endpoints.Account.Lists.History import History
from Endpoints.Account.Lists.Whitelist import Whitelist
from Endpoints.Account.Lists.Blacklist import Blacklist
# Delete unique endpoint import
from Endpoints.Account.DeleteAccount import DeleteAccount

class InitAccountEndpoints():
    def __init__(self, Api):
        self.__InitInfosEndpoints(Api)
        self.__InitListsEndpoints(Api)
        self.__InitDeleteEndpoint(Api)


    def __InitInfosEndpoints(self, Api):
        Api.add_resource(GetInfos, "/account/infos/getInfos")
        Api.add_resource(UpdateEmail, "/account/infos/updateEmail")
        Api.add_resource(UpdatePersonalInfos, "/account/infos/update-infos")


    def __InitListsEndpoints(self, Api):
        Api.add_resource(GreyList, "/account/lists/greylist")
        Api.add_resource(History, "/account/lists/history")
        Api.add_resource(Whitelist, "/account/lists/whitelist")
        Api.add_resource(Blacklist, "/account/lists/blacklist")


    def __InitDeleteEndpoint(self, Api):
        Api.add_resource(DeleteAccount, "/account/delete")
