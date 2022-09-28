##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## TellowsNumberEvaluation
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class InternalNumberEvaluation(JParent):
    def __init__(self, number: str, score: int, calls: int, reports: int, blocked: int):
        self.__InitJParent(number, score, calls, reports, blocked)

    # Values Assignement
    def __InitJParent(self, number: str, score: int, calls: int, reports: int, blocked: int):
        self.number = number
        self.score = score
        self.calls = calls
        self.blocked = blocked
        self.reports = reports

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.number is None): return "Internal Error - Missing Number"
        if (type(self.number) is not str): return "Internal Error - Invalid Number"

        if (self.score is None): return "Internal Error - Missing Score"
        if (type(self.score) is not int): return "Internal Error - Invalid Score"

        if (self.calls is None): return "Internal Error - Missing Calls"
        if (type(self.calls) is not int): return "Internal Error - Invalid Calls"

        if (self.blocked is None): return "Internal Error - Missing Blocked"
        if (type(self.blocked) is not int): return "Internal Error - Invalid Blocked"

        if (self.reports is None): return "Internal Error - Missing Reports"
        if (type(self.reports) is not int): return "Internal Error - Invalid Reports"
        return None
