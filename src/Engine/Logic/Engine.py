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

### MODELS
# CallStatus Enum
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus
# Box Model import
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity


### /!\ WARNING /!\ ###
# This is the ONLY way to interact with the Engine, proceed with caution
### /!\ WARNING /!\ ###


## TODO: redo the errors with a real Error Mangaer


# This is the engine of Magi to evaluate the calls & numbers
class Engine():
    def __init__(self):
        self.__Tellows = Tellows()
        self.__NumberDB = NumberDB("FR-0033", "0033")

    ### PUBLIC

    # Just veify the number
    def Verify(self, User: User, boxid: str, number: str):
        # TODO: 1 - If the number is not in our DB, create it with a perfect score

        UserBox:Box = User.Box.PullBox(boxid)

        if (UserBox is None):
            return "Unknown Box"

        return self.__EvaBoxAlgorithm(
            UserBox.severity,
            number
        )


    # At the end of the call, report or not, status of the call
    def ProcessCall(self, User: User, boxid: str, Status: CallStatus, report: bool, number: str):
        # TODO: 1.1 - Block for the user if not in blacklist
        # TODO: 1.2 - Unblock for the user if in the blacklist & return

        # TODO: 2.0 - Save the call to the history

        # TODO: 3.0 - Report the number

        # TODO: 4.0 - Evaluate the number, if already reported or just create the case
        return

    ### PRIVATE
    def __EvaBoxAlgorithm(self, severity: BoxSeverity, number: str):
        if (severity is BoxSeverity.NONE):
            return False
        elif (severity is BoxSeverity.BLACKLIST):
            return True
        elif (severity is BoxSeverity.NORMAL):
            return True
        elif (severity is BoxSeverity.HIGH):
            return True
        elif (severity is BoxSeverity.MAX):
            return True
        return None
