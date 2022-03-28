##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BoxInfosResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Import object of list
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
# Enum import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity

# Represents Box Infos Response
class BoxInfosResponse(JParent):
    def __init__(self, Boxes: list):
        self.__InitJParent(Boxes)

    # Values Assignement
    def __InitJParent(self, Boxes: list):
        self.Boxes = []
        for Bx in Boxes:
            self.Boxes.append(
                self.__CreateHCbasic(Bx)
            )


    def __CreateHCbasic(self, Bx: Box):
        return {
            "boxid": Bx.boxid,
            "activity": Bx.activity,
            "severity": BoxSeverity.EnumToStr(Bx.severity)
        }


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.Boxes is None): return "Internal Model Error"
        if (type(self.Boxes) is not list): return "Internal Model Error"
        return None
