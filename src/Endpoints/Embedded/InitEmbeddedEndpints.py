##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEmbeddedEndpints
##

### INFRA
# Login box unique endpoint import
from Endpoints.Embedded.LoginBox import LoginBox
# Link box unique endpoint import
from Endpoints.Embedded.LinkBox import LinkBox
# Infos box unique endpoint import
from Endpoints.Embedded.BoxInfos import BoxInfos
# Avaible Update unique endpoint import
from Endpoints.Embedded.AvaibleUpdate import AvaiableUpdate


# Initialization of the endpoints for emebeded side
class InitEmbeddedEndpoints():
    def __init__(self, Api):
        self.__InitLoginBoxEndpoint(Api)
        self.__InitLinkBoxEndpoint(Api)
        self.__InitBoxInfosEndpoint(Api)
        self.__InitAvaibleUpdateEndpoint(Api)

    def __InitLoginBoxEndpoint(self, Api):
        Api.add_resource(LoginBox, "/embedded/login-box")


    def __InitLinkBoxEndpoint(self, Api):
        Api.add_resource(LinkBox, "/embedded/link-box")


    def __InitBoxInfosEndpoint(self, Api):
        Api.add_resource(BoxInfos, "/embedded/box-infos")


    def __InitAvaibleUpdateEndpoint(self, Api):
        Api.add_resource(AvaiableUpdate, "/embedded/update")
