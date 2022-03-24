##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEmbeddedEndpints
##

### INFRA
# Link endpoint imports
from Endpoints.Embedded.Link.ClaimBox import ClaimBox
# Login box unique endpoint import
from Endpoints.Embedded.LoginBox import LoginBox
# Infos box unique endpoint import
from Endpoints.Embedded.BoxInfos import BoxInfos
# Avaible Update unique endpoint import
from Endpoints.Embedded.AvailableUpdate import AvaiableUpdate


# Initialization of the endpoints for emebeded side
class InitEmbeddedEndpoints():
    def __init__(self, Api):
        self.__InitLinkEndpoints(Api)
        self.__InitLoginBoxEndpoint(Api)
        self.__InitBoxInfosEndpoint(Api)
        self.__InitAvaiableUpdateEndpoint(Api)


    def __InitLinkEndpoints(self, Api):
        Api.add_resource(ClaimBox, "/embedded/link/claim-box")


    def __InitLoginBoxEndpoint(self, Api):
        Api.add_resource(LoginBox, "/embedded/login")


    def __InitBoxInfosEndpoint(self, Api):
        Api.add_resource(BoxInfos, "/embedded/box-infos")


    def __InitAvaiableUpdateEndpoint(self, Api):
        Api.add_resource(AvaiableUpdate, "/embedded/update")
