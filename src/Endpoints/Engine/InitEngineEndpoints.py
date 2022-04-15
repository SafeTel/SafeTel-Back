##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEngineEndpoints
##

### INFRA
# Evaluate Number unique endpoint import
from Endpoints.Engine.EvaluateNumber import EvaluateNumber

class InitEngineEndpoints():
    def __init__(self, Api):
        self.ENGINE_URI_BASE_DOMAIN = "/engine/"
        self.__InitEvaluateNumberEndpoint(Api)


    def __InitEvaluateNumberEndpoint(self, Api):
        Api.add_resource(
            EvaluateNumber,
            self.ENGINE_URI_BASE_DOMAIN + "evaluate-number"
        )
