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
from Endpoints.Account.Infos.ChangePersonalInfos import ChangesPersonalInfos
# Lists endpoints imports
from Endpoints.Account.Lists.GreyList.GetGreyList import GetGreyList
from Endpoints.Account.Lists.History.GetHistory import GetHistory
from Endpoints.Account.Lists.History.DelHistory import DelHistory
from Endpoints.Account.Lists.History.AddHistory import AddHistory
from Endpoints.Account.Lists.WhiteList.GetWhiteList import GetWhiteList
from Endpoints.Account.Lists.WhiteList.DelWhiteList import DelWhiteList
from Endpoints.Account.Lists.WhiteList.AddWhiteList import AddWhiteList
from Endpoints.Account.Lists.BlackList.GetBlackList import GetBlackList
from Endpoints.Account.Lists.BlackList.DelBlackList import DelBlackList
from Endpoints.Account.Lists.BlackList.AddBlackList import AddBlackList
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
        Api.add_resource(ChangesPersonalInfos, "/account/infos/update-infos")


    def __InitListsEndpoints(self, Api):
        Api.add_resource(GetGreyList, "/account/lists/greylist")
        Api.add_resource(GetHistory, "/account/lists/history")
        Api.add_resource(DelHistory, "/account/lists/history")
        Api.add_resource(AddHistory, "/account/lists/history")
        Api.add_resource(GetWhiteList, "/account/lists/whitelist")
        Api.add_resource(DelWhiteList, "/account/lists/whitelist")
        Api.add_resource(AddWhiteList, "/account/lists/whitelist")
        Api.add_resource(GetBlackList, "/account/lists/blacklist")
        Api.add_resource(DelBlackList, "/account/lists/blacklist")
        Api.add_resource(AddBlackList, "/account/lists/blacklist")


    def __InitDeleteEndpoint(self, Api):
        Api.add_resource(DeleteAccount, "/account/delete")
