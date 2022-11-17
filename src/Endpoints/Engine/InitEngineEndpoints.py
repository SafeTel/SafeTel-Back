##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitEngineEndpoints
##

### INFRA
# Verify Number unique endpoint import
from Endpoints.Engine.VerifyNumber import VerifyNumber
# Evaluate Call unique endpoint import
from Endpoints.Engine.EvaluateCall import EvaluateCall
# Evaluate Call unique endpoint import
from Endpoints.Engine.ReportedCount import ReportedCount
# Send back reported numbers
from Endpoints.Engine.GetReportedNumbers import GetReportedNumbers


class InitEngineEndpoints():
    def __init__(self, Api):
        self.ENGINE_URI_BASE_DOMAIN = "/engine/"
        self.__InitVerifyNumberEndpoint(Api)
        self.__InitEvaluateCallEndpoint(Api)
        self.__InitReportedCountEndpoint(Api)
        self.__InitGetReportedNumbersEndpoint(Api)


    def __InitVerifyNumberEndpoint(self, Api):
        Api.add_resource(
            VerifyNumber,
            self.ENGINE_URI_BASE_DOMAIN + "verify-number"
        )

    def __InitEvaluateCallEndpoint(self, Api):
        Api.add_resource(
            EvaluateCall,
            self.ENGINE_URI_BASE_DOMAIN + "evaluate-call"
        )

    def __InitReportedCountEndpoint(self, Api):
        Api.add_resource(
            ReportedCount,
            self.ENGINE_URI_BASE_DOMAIN + "reported-count"
        )

    def __InitGetReportedNumbersEndpoint(self, Api):
        Api.add_resource(
            GetReportedNumbers,
            self.ENGINE_URI_BASE_DOMAIN + "get-reported-numbers"
        )
