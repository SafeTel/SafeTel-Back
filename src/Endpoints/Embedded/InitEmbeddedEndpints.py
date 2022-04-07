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
from Endpoints.Embedded.UpdateActivity import UpdateActivity
# Avaible Update unique endpoint import
from Endpoints.Embedded.UpdateSeverity import UpdateSeverity
# Avaible Update unique endpoint import
from Endpoints.Embedded.AvailableUpdate import AvaiableUpdate


# Initialization of the endpoints for emebeded side
class InitEmbeddedEndpoints():
    def __init__(self, Api):
        self.EMBEDDED_URI_BASE_DOMAIN = "/embedded/"
        self.__InitLinkEndpoints(Api)
        self.__InitLoginBoxEndpoint(Api)
        self.__InitBoxInfosEndpoint(Api)
        self.__InitUpdateActivityEndpoint(Api)
        self.__InitUpdateSeverityEndpoint(Api)
        self.__InitAvaiableUpdateEndpoint(Api)


    def __InitLinkEndpoints(self, Api):
        Api.add_resource(
            ClaimBox,
            self.EMBEDDED_URI_BASE_DOMAIN + "link/claim-box"
        )


    def __InitLoginBoxEndpoint(self, Api):
        Api.add_resource(
            LoginBox,
            self.EMBEDDED_URI_BASE_DOMAIN + "login-box"
        )


    def __InitBoxInfosEndpoint(self, Api):
        Api.add_resource(
            BoxInfos,
            self.EMBEDDED_URI_BASE_DOMAIN + "box-infos"
        )


    def __InitUpdateActivityEndpoint(self, Api):
        Api.add_resource(
            UpdateActivity,
            self.EMBEDDED_URI_BASE_DOMAIN + "update-activity"
        )


    def __InitUpdateSeverityEndpoint(self, Api):
        Api.add_resource(
            UpdateSeverity,
            self.EMBEDDED_URI_BASE_DOMAIN + "update-severity"
        )


    def __InitAvaiableUpdateEndpoint(self, Api):
        Api.add_resource(
            AvaiableUpdate,
            self.EMBEDDED_URI_BASE_DOMAIN + "update"
        )
