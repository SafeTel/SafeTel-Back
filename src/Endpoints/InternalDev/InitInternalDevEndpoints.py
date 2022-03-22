##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## InitInternalDevEndpoints
##

### INFRA
# Account endpoints import
from Endpoints.InternalDev.Account.RegisterAdminDev import RegisterAdminDev
from Endpoints.InternalDev.Account.ClaimApiKeys import ClaimApiKeys
# Health Check unique endpoint import
from Endpoints.InternalDev.HealthCheck import HealthCheck

class InitInternalDevEndpoints():
    def __init__(self, Api):
        self.__InitAccountEndpoints(Api)
        self.__InitHealthCheckEndpoint(Api)


    def __InitAccountEndpoints(self, Api):
        Api.add_resource(RegisterAdminDev, "/internaldev/account/register")
        Api.add_resource(ClaimApiKeys, "/internaldev/account/claimApiKey")

    def __InitHealthCheckEndpoint(self, Api):
        Api.add_resource(HealthCheck, "/internaldev/healthCheck")
