##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitAuthEndpoints
##

### INFRA
# Token endpoints import
from Endpoints.Authentification.Token.CheckToken import CheckToken
from Endpoints.Authentification.Token.ResetToken import ResetToken
# LostPassword endpoints import
from Endpoints.Authentification.LostPassword.ResetPassword import ResetPassword
from Endpoints.Authentification.LostPassword.UpdateLostPassword import UpdateLostPassword
# Register unique endpoint import
from Endpoints.Authentification.Register import Register
# Login unique endpoint import
from Endpoints.Authentification.Login import Login

class InitAuthentificationEndpoints():
    def __init__(self, Api):
        self.__InitLostPasswordEndpoints(Api)
        self.__InitCheckTokenEndpoints(Api)
        self.__InitRegisterEndpoint(Api)
        self.__InitLoginEndpoint(Api)


    def __InitLostPasswordEndpoints(self, Api):
        Api.add_resource(ResetPassword, "/auth/lost-password/reset-password")
        Api.add_resource(UpdateLostPassword, "/auth/lost-password/update-password")


    def __InitCheckTokenEndpoints(self, Api):
        Api.add_resource(CheckToken, "/auth/token/check-token")
        Api.add_resource(ResetToken, "/auth/token/reset-token")


    def __InitRegisterEndpoint(self, Api):
        Api.add_resource(Register, "/auth/register")


    def __InitLoginEndpoint(self, Api):
        Api.add_resource(Login, "/auth/login")
