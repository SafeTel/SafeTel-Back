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
### LOGIC
# Evaluators
from Engine.Logic.InternalEvaluator import InternalEvaluator
from Engine.Logic.TellowsEvaluator import TellowsEvaluator



# This part of the engine is responsible for rating the score of each number
class RateNumber():
    def __init__(self):
        self.__InternalEvaluator = InternalEvaluator()
        self.__TellowsEvaluator = TellowsEvaluator()

    ### PUBLIC

    # Evaluate a number, 1 to 10, higher is better
    def EvaNumber(self, number: str, InternalData: dict):
        if ("TellowsResponse" not in InternalData):
            return None

        InternalScore, InternalCoefficient = self.__InternalEvaluator.EvaNumber(number, InternalData)
        TellowsData :TellowsNumberEvaluation = self.__TellowsEvaluator.EvaNumber(number, InternalData)

        MergedScore = self.__MergeScores(
            TellowsData,
            InternalScore,
            InternalCoefficient
        )

        return int(MergedScore)


    ### PRIVATE

    def __MergeScores(self, TellowsData: TellowsNumberEvaluation, InternalScore: float, InternalCoefficient: float):
        InternalDataConsistency = self.__IsInternalDataConsistent(InternalCoefficient)

        if (not InternalDataConsistency):
            return 5

        InternalScale = self.__EvaInternalScale(InternalScore, InternalCoefficient)
        TellowsScale = TellowsData.searches

        MergedScore = (InternalScale + TellowsScale) / (InternalCoefficient * TellowsData.searches)

        if (MergedScore > 10):
            MergedScore = 10

        return MergedScore


    def __IsInternalDataConsistent(self, InternalCoefficient: float):
        if (InternalCoefficient > 10):
            return True
        return False


    def __EvaInternalScale(self, InternalScore: float, InternalCoefficient: float):
        return InternalScore * InternalCoefficient


    ### UTILS

    def __PercentValue(self, interest: int, subject: int):
        return int((interest / subject) * 100)
