##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEmbeddedEndpints
##

### INFRA
# Login box unique endpoint import
from Endpoints.Embedded.LoginBox import LoginBox
# Rverse Report unique endpoint import
from Endpoints.Embedded.ReverseEvaluation import ReverseEvaluation


# Initialization of the endpoints for emebeded side
class InitEmbeddedEndpoints():
    def __init__(self, Api):
        self.EMBEDDED_URI_BASE_DOMAIN = "/embedded/"
        self.__InitLoginBoxEndpoint(Api)
        self.__InitReverseReportEndpoint(Api)


    def __InitLoginBoxEndpoint(self, Api):
        Api.add_resource(
            LoginBox,
            self.EMBEDDED_URI_BASE_DOMAIN + "login-box"
        )


    def __InitReverseReportEndpoint(self, Api):
        Api.add_resource(
            ReverseEvaluation,
            self.EMBEDDED_URI_BASE_DOMAIN + "reverse-evaluation"
        )
