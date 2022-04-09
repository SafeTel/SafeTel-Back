##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitAccountEndpoints
##

### INFRA
# Infos endpoint imports
from Endpoints.Account.Infos.GetInfos import GetInfos
from Endpoints.Account.Infos.UpdateEmail import UpdateEmail
from Endpoints.Account.Infos.UpdatePersonalInfos import UpdatePersonalInfos
from Endpoints.Account.Infos.UpdatePassword import UpdatePassword
# Lists endpoints imports
from Endpoints.Account.Lists.Greylist import GreyList
from Endpoints.Account.Lists.History import History
from Endpoints.Account.Lists.Whitelist import Whitelist
from Endpoints.Account.Lists.Blacklist import Blacklist
# Delete unique endpoint import
from Endpoints.Account.DeleteAccount import DeleteAccount

class InitAccountEndpoints():
    def __init__(self, Api):
        self.ACCOUNT_URI_BASE_DOMAIN = "/account/"
        self.__InitInfosEndpoints(Api)
        self.__InitListsEndpoints(Api)
        self.__InitUniqueEndpoint(Api)


    def __InitInfosEndpoints(self, Api):
        Api.add_resource(
            GetInfos,
            self.ACCOUNT_URI_BASE_DOMAIN + "infos/get-infos"
        )
        Api.add_resource(
            UpdateEmail,
            self.ACCOUNT_URI_BASE_DOMAIN + "infos/update-email"
        )
        Api.add_resource(
            UpdatePersonalInfos,
            self.ACCOUNT_URI_BASE_DOMAIN + "infos/update-infos"
        )
        Api.add_resource(
            UpdatePassword,
            self.ACCOUNT_URI_BASE_DOMAIN + "infos/update-password"
        )


    def __InitListsEndpoints(self, Api):
        Api.add_resource(
            Blacklist,
            self.ACCOUNT_URI_BASE_DOMAIN + "lists/blacklist"
        )
        Api.add_resource(
            Whitelist,
            self.ACCOUNT_URI_BASE_DOMAIN + "lists/whitelist")
        Api.add_resource(
            GreyList,
            self.ACCOUNT_URI_BASE_DOMAIN + "lists/greylist"
        )
        Api.add_resource(
            History,
            "/account/lists/history"
        )


    def __InitUniqueEndpoint(self, Api):
        Api.add_resource(
            DeleteAccount,
            self.ACCOUNT_URI_BASE_DOMAIN + "delete"
        )
