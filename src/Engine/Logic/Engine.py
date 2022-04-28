##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Engine
##

### INFRA
# User sub class import
from Infrastructure.Factory.UserFactory.User import User
# Tellows service
from Engine.Infrastructure.Services.Tellows import Tellows
# DataBase service
from Engine.Infrastructure.DataBase.NumberDB import NumberDB

class Engine():
    def __init__(self):
        self.__Tellows = Tellows()
        self.__NumberDB = NumberDB("FR-0033", "0033")


    def Verify(self, User: User, boxid: str, number: str):
        # TODO: evaluate the number, next task
        # TODO: if malicious number block the number for the user

        # TODO: else just dont block it
        return


    def Report(self, User: User, number: str):
        # TODO: block for the user
        # TODO: report the number
        # TODO: evaluate the number, if already reported or just create the case
        return
