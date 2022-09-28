##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## InternalEvaluator
##

### MODELS
# Evaluation Models
from Engine.Models.NumberEvaluation.InternalNumberEvaluation import InternalNumberEvaluation


# This part of the engine is responsible for rating the score of each number
class InternalEvaluator():
    def __init__(self):
        return

    ### PUBLIC

    # Evaluate a number, 1 to 10, higher is better
    def EvaNumber(self, number: str, InternalData: dict):
        if ("TellowsResponse" not in InternalData):
            return None

        InternalEvaluation :InternalNumberEvaluation = self.__ExtractInternalData(number, InternalData)
        InternalScore, InternalCoefficient = self.__EvaInternalData(InternalEvaluation)

        return InternalScore, InternalCoefficient


    ### PRIVATE

    def __ExtractInternalData(self, number, InternalData: dict):
        InternalEvaluation = InternalNumberEvaluation(
            number,
            InternalData["score"],
            InternalData["calls"],
            InternalData["reportedcalls"],
            InternalData["blockedcalls"]
        )
        modelErrors = InternalEvaluation.EvaluateModelErrors()
        if (modelErrors != None):
            return None
        return InternalEvaluation


    def __EvaInternalData(self, InternalData: InternalNumberEvaluation):
        if (InternalData.calls < 10):
            return 5, InternalData.calls

        reportedCallsPercent = self.__PercentValue(
            InternalData.reports,
            InternalData.calls
        )
        return 10 - (reportedCallsPercent / 10), InternalData.calls


    ### UTILS

    def __PercentValue(self, interest: int, subject: int):
        return int((interest / subject) * 100)
