##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitBoxEndpints
##

### INFRA
# Link endpoint imports
from Endpoints.Box.Link.ClaimBox import ClaimBox
# Infos box unique endpoint import
from Endpoints.Box.BoxInfos import BoxInfos
# Avaible Update unique endpoint import
from Endpoints.Box.UpdateActivity import UpdateActivity
# Avaible Update unique endpoint import
from Endpoints.Box.UpdateSeverity import UpdateSeverity


# Initialization of the endpoints for emebeded side
class InitBoxEndpints():
    def __init__(self, Api):
        self.BOX_URI_BASE_DOMAIN = "/box/"
        self.BOX_URI_LINK_DOMAIN = "link/"
        self.__InitLinkEndpoints(Api)
        self.__InitBoxInfosEndpoint(Api)
        self.__InitUpdateActivityEndpoint(Api)
        self.__InitUpdateSeverityEndpoint(Api)


    def __InitLinkEndpoints(self, Api):
        Api.add_resource(
            ClaimBox,
            self.BOX_URI_BASE_DOMAIN + self.BOX_URI_LINK_DOMAIN + "claim-box"
        )


    def __InitBoxInfosEndpoint(self, Api):
        Api.add_resource(
            BoxInfos,
            self.BOX_URI_BASE_DOMAIN + "box-infos"
        )


    def __InitUpdateActivityEndpoint(self, Api):
        Api.add_resource(
            UpdateActivity,
            self.BOX_URI_BASE_DOMAIN + "update-activity"
        )


    def __InitUpdateSeverityEndpoint(self, Api):
        Api.add_resource(
            UpdateSeverity,
            self.BOX_URI_BASE_DOMAIN + "update-severity"
        )
