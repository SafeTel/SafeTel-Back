##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## TellowsEvaluator
##

### MODELS
# Evaluation Models
from Engine.Models.NumberEvaluation.TellowsNumberEvaluation import TellowsNumberEvaluation


# This part of the engine is responsible for rating the score of each number
class TellowsEvaluator():
    def __init__(self):
        return

    ### PUBLIC

    # Evaluate a number, 1 to 10, higher is better
    def EvaNumber(self, number: str, InternalData: dict):
        if ("TellowsResponse" not in InternalData):
            return None

        TellowsData :TellowsNumberEvaluation = self.__ExtractTellowsData(number, InternalData["TellowsResponse"])

        return TellowsData


    ### PRIVATE

    def __ExtractTellowsData(self, number: str, TellowsData: dict):
        if (TellowsData is None):
            return None
        TellowsEvaluation = TellowsNumberEvaluation(
            number,
            10 - int(TellowsData["score"]),
            int(TellowsData["searches"]),
            int(TellowsData["comments"])
        )
        modelErrors = TellowsEvaluation.EvaluateModelErrors()
        if (modelErrors != None):
            return None
        return TellowsEvaluation


    ### UTILS

    def __PercentValue(self, interest: int, subject: int):
        return int((interest / subject) * 100)
