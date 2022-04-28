##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BlockAlgorithms
##

### INFRA
# User sub class import
from Infrastructure.Factory.UserFactory.User import User
# DataBase service
from Engine.Infrastructure.DataBase.NumberDB import NumberDB

# Pick the algorithm for evey case
class BlockAlgorithm():
    def __init__(self):
        self.__NumberDB = NumberDB("FR-0033", "0033")

    ### PUBLIC

    def BlockBlacklist(self, User: User, number: str):
        return self.IsBlacklisted(User, number)


    def BlockNormal(self, User: User, number: str):
        if (self.IsBlacklisted(User, number)):
            return True

        score = self.__NumberDB.getNumber(number)["score"]
        if (score == None):
            return "Internal Error - Unknown Number in DB"

        if (score < 5):
            return True
        return False


    def BlockHigh(self, User: User, number: str):
        if (self.IsBlacklisted(User, number)):
            return True

        score = self.__NumberDB.getNumber(number)["score"]
        if (score == None):
            return "Internal Error - Unknown Number in DB"

        if (score < 7):
            return True
        return False


    def BlockMax(self, User: User, number: str):
        return self.IsWhitelisted(User, number)


    ### PRIVATE

    def IsBlacklisted(self, User: User, number: str):
        if (User.Blacklist.IsNumber(number)):
            return True
        return False


    def IsWhitelisted(self, User: User, number: str):
        if (User.Whitelist.IsNumber(number)):
            return True
        return False
