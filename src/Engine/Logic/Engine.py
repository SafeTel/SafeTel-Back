##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Engine
##

### INFRA
# User sub class import
from tokenize import Number
from Infrastructure.Factory.UserFactory.User import User
# Tellows service
from Engine.Infrastructure.Services.Tellows import Tellows
# DataBase service
from Engine.Infrastructure.DataBase.NumberDB import NumberDB

### LOGIC
# Block algorithms import
from Engine.Logic.BlockAlgorithm import BlockAlgorithm
# Rate Number algorithm
from Engine.Logic.RateNumber import RateNumber

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


# This is the engine of Magi to evaluate the calls & numbers
class Engine():
    def __init__(self):
        self.__Tellows = Tellows()
        self.__NumberDB = NumberDB("FR-0033", "0033")
        self.__BlockAlgorithm = BlockAlgorithm()
        self.__RateNumber = RateNumber()

    ### PUBLIC

    def ReportedCount(self):
        return self.__NumberDB.count()


    def GetReportedNumbers(self, index: int):
        Result :list = []
        RangeMinimal :int = (index - 1) * 3
        RangeMaximal :int = index * 3

        Cursor = list(self.__NumberDB.getNumbers())

        if (len(Cursor) < RangeMinimal):
            return Result

        if (len(Cursor) < RangeMaximal):
            RangedCursor = Cursor[RangeMinimal : len(Cursor) - 1]
        else:
            RangedCursor = Cursor[RangeMinimal : RangeMaximal]

        for Document in RangedCursor:
            if (Document["score"] > 5):
                Result.append(Document["number"])

        return Result


    # Just veify the number
    def Verify(self, User: User, boxid: str, number: str):
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

        if (self.__IsNumberReportedByUser(User.GetGUID(), HistoryCall.number)):
            return "Number already reported by the user"

        if (HistoryCall.status is CallStatus.BLOCKED):
            self.__NumberDB.addBlockedCall(HistoryCall.number)
            return "Number has already been blocked, report this bug"

        if (report):
            self.__NumberDB.reportNumber(
                HistoryCall.number,
                User.GetGUID(),
                boxid
            )
            User.Blacklist.AddNumber(HistoryCall.number)
        else:
            self.__NumberDB.addCall(HistoryCall.number)

        InternalData = self.__NumberDB.getNumber(HistoryCall.number)
        NewScore = self.__RateNumber.EvaNumber(
            HistoryCall.number,
            InternalData
        )

        self.__NumberDB.UpdateScore(
            HistoryCall.number,
            NewScore
        )

        return "OK"


    ### PRIVATE

    def __IsNumberReportedByUser(self, guid: str, number: str):
        for Report in self.__NumberDB.getNumber(number)["Reports"]:
            if (Report["guid"] == guid):
                return True
        return False


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
        User.Box.UpdateSeverity("normal")
        return None
