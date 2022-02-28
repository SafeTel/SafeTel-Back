##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InitEngineEndpoints
##

### INFRA
# Tellows evaluation unique endpoint import
from Endpoints.Engine.Tellows.GetTellows import GetTellows

class InitEngineEndpoints():
    def __init__(self, Api):
        self.__InitTellowsEvaEndpoint(Api)


    def __InitTellowsEvaEndpoint(self, Api):
        Api.add_resource(GetTellows, "/engine/tellows")
