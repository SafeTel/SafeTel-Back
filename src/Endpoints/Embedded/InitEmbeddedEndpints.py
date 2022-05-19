##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEmbeddedEndpints
##

### INFRA
# Login box unique endpoint import
from Endpoints.Embedded.LoginBox import LoginBox
# Reverse Evaluation unique endpoint import
from Endpoints.Embedded.ReverseEvaluation import ReverseEvaluation
# Reset Embedded Token unique endpoint import
from Endpoints.Embedded.Token.ResetEmbeddedToken import ResetEmbeddedToken


# Initialization of the endpoints for emebeded side
class InitEmbeddedEndpoints():
    def __init__(self, Api):
        self.EMBEDDED_URI_BASE_DOMAIN = "/embedded/"
        self.EMBEDDED_URI_TOKEN_DOMAIN = "token/"
        self.__InitLoginBoxEndpoint(Api)
        self.__InitReverseReportEndpoint(Api)
        self.__InitResetEmbeddedTokenEndpoint(Api)


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


    def __InitResetEmbeddedTokenEndpoint(self, Api):
        Api.add_resource(
            ResetEmbeddedToken,
            self.EMBEDDED_URI_BASE_DOMAIN + self.EMBEDDED_URI_TOKEN_DOMAIN + "reset-embedded-token"
        )
