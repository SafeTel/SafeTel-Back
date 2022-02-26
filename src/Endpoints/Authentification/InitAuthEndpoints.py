##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitAuthEndpoints
##

### INFRA
# Check Token unique endpoint import
from Endpoints.Authentification.CheckToken import CheckToken
# Reset Token unique endpoint import
from Endpoints.Authentification.ResetToken import ResetToken
# Register unique endpoint import
from Endpoints.Authentification.Register import Register
# Login unique endpoint import
from Endpoints.Authentification.Login import Login

class InitAuthentificationEndpoints():
    def __init__(self, Api):
        self.__InitCheckTokenEndpoint(Api)
        self.__InitResetTokenEndpoint(Api)
        self.__InitRegisterEndpoint(Api)
        self.__InitLoginEndpoint(Api)


    def __InitCheckTokenEndpoint(self, Api):
        Api.add_resource(CheckToken, "/auth/check-token")


    def __InitResetTokenEndpoint(self, Api):
        Api.add_resource(ResetToken, "/auth/reset-token")


    def __InitRegisterEndpoint(self, Api):
        Api.add_resource(Register, "/auth/register")


    def __InitLoginEndpoint(self, Api):
        Api.add_resource(Login, "/auth/login")
