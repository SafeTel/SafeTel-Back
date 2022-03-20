##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEmbededEndpints
##

### INFRA
# Login box unique endpoint import
from Endpoints.Embeded.LoginBox import LoginBox
# Link box unique endpoint import
from Endpoints.Embeded.LinkBox import LinkBox
# Infos box unique endpoint immport
from Endpoints.Embeded.BoxInfos import BoxInfos

# Initialization of the endpoints for emebeded side
class InitEmbededEndpoints():
    def __init__(self, Api):
        self.__InitLoginBoxEndpoint(Api)
        self.__InitLinkBoxEndpoint(Api)
        self.__InitBoxInfosEndpoint(Api)

    def __InitLoginBoxEndpoint(self, Api):
        Api.add_resource(LoginBox, "/embeded/login-box")


    def __InitLinkBoxEndpoint(self, Api):
        Api.add_resource(LinkBox, "/embeded/link-box")


    def __InitBoxInfosEndpoint(self, Api):
        Api.add_resource(BoxInfos, "/embeded/box-infos")
