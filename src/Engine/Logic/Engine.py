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

### LOGIC
# Block algorithms import
from Engine.Logic.BlockAlgorithm import BlockAlgorithm

### MODELS
# CallStatus Enum
from Models.Endpoints.SharedJObject.Account.Lists.CallStatus import CallStatus
# Box Model import
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity
# Sub Model for HistoryCall Request import
from Models.Endpoints.Account.Lists.History.HistoryCallRequest import HistoryCallRequest


### /!\ WARNING /!\ ###
# This is the ONLY way to interact with the Engine, proceed with caution
### /!\ WARNING /!\ ###


## TODO: redo the errors with a real Error Mangaer FIXME: next sprint
# This is the engine of Magi to evaluate the calls & numbers
class Engine():
    def __init__(self):
        self.__Tellows = Tellows()
        self.__NumberDB = NumberDB("FR-0033", "0033")
        self.__BlockAlgorithm = BlockAlgorithm()

    ### PUBLIC

    # Just veify the number
    def Verify(self, User: User, boxid: str, number: str):
        # TODO: Verify the number country by regex FIXME: next sprint
        TellowsResponse = self.__Tellows.GetEvaluation(number)
        if (TellowsResponse is None):
            return "Internal Error"

        if (not self.__NumberDB.isNumber(number)):
            score = 5
            if (TellowsResponse["score"] != 5):
                score = TellowsResponse["score"]

            self.__NumberDB.addNumberWithoutReport(
                number,
                TellowsResponse,
                score
            )
        else:
            self.__NumberDB.addCall(number)

        UserBox:Box = User.Box.PullBox(boxid)
        if (UserBox is None):
            return "Unknown Box"

        return self.__EvaBoxAlgorithm(
            User,
            UserBox.severity,
            number
        )


    # At the end of the call, process the call & act
    def ProcessCall(self, User: User, boxid: str, report: bool, HistoryCall: HistoryCallRequest):
        User.History.AddHistoryCall(HistoryCall)

        if (report and User.Blacklist.IsNumber(HistoryCall.number)):
            return User.Blacklist.DeleteNumber(HistoryCall.number)

        if (report):
            self.__NumberDB.reportNumber(
                HistoryCall.number,
                User.__guid,
                boxid
            )
            User.Blacklist.AddNumber(HistoryCall.number)

        # TODO: 4.0 - Revaluate the number FIXME: next task
        return User.Blacklist.PullList()

    ### PRIVATE

    def __EvaBoxAlgorithm(self, User: User,  severity: BoxSeverity, number: str):
        if (severity is BoxSeverity.NONE):
            return False
        elif (severity is BoxSeverity.BLACKLIST):
            return  self.__BlockAlgorithm.BlockBlacklist(User, number)
        elif (severity is BoxSeverity.NORMAL):
            return  self.__BlockAlgorithm.BlockNormal(User, number)
        elif (severity is BoxSeverity.HIGH):
            return  self.__BlockAlgorithm.BlockHigh(User, number)
        elif (severity is BoxSeverity.MAX):
            return  self.__BlockAlgorithm.BlockMax(User, number)
        return None
        # TODO: None, means there is a bug internal error (the severity is corrupted)
        # FIXME: maybe autofix ?
