##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## RateNumber
##

### MODELS
# Evaluation Models
from Engine.Models.NumberEvaluation.InternalNumberEvaluation import InternalNumberEvaluation
from Engine.Models.NumberEvaluation.TellowsNumberEvaluation import TellowsNumberEvaluation


# This part of the engine is responsible for rating the score of each number
# TODO: Takes models as arguments
class RateNumber():
    def __init__(self):
        return

    ### PUBLIC

    # Evaluate a number, 1 to 10, higher is better
    def EvaNumber(self, number: str, InternalData: dict):
        if ("TellowsResponse" not in InternalData): # TODO: faire un report d'erreur au monitoring si manque de données FIXME: next sprint
            return None

        TellowsEvaluation :TellowsNumberEvaluation = self.__ExtTellowsData(number, InternalData["TellowsResponse"])
        InternalEvaluation :InternalNumberEvaluation = self.__ExtInternalData(number, InternalData)

        InternalScore, InternalCoefficient = self.__EvaInternalData(InternalEvaluation)

        # 3 - Merge les 2 notes en fonction des coeficients
        MergedScore = self.__MergeScores(
            TellowsEvaluation,
            InternalScore,
            InternalCoefficient
        )

        return int(MergedScore)


    ### PRIVATE

    def __MergeScores(self, TellowsEvaluation: TellowsNumberEvaluation, InternalScore: float, InternalCoefficient: float):
        InternalScale = InternalScore * InternalCoefficient
        TellowsScale = TellowsEvaluation.score * TellowsEvaluation.searches
        MergedScore = (InternalScale + TellowsScale) / (InternalCoefficient * TellowsEvaluation.searches)
        return MergedScore


    def __EvaInternalData(self, InternalData: InternalNumberEvaluation):
        reportedCallsPercent = self.__PercentValue(
            InternalData.reports,
            InternalData.calls
        )
        return (reportedCallsPercent / 10), InternalData.calls


    def __ExtInternalData(self, number, InternalData: dict):
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


    def __ExtTellowsData(self, number: str, TellowsData: dict):
        if (TellowsData is None):
            return None
        TellowsEvaluation = TellowsNumberEvaluation(
            number,
            int(TellowsData["score"]),
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
