##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## BoxList
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Model Shared import
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
# Shared Enum import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity

# Represents Number Request
class BoxList(JObject):
    def __init__(self, Boxes: list):
        self.__InitJObject(Boxes)


    # Values Assignement
    def __InitJObject(self, Boxes: list):
        self.Boxes = []
        for Box in Boxes:
            self.Boxes.append(
                Box(
                    Box["boxid"],
                    Box["activity"],
                    BoxSeverity.StrToEnum(Box["severity"])
            ))


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None


    def __EvaErrorsJParent(self):
        if (self.Boxes is None): return "Internal Model Error"
        if (type(self.Boxes) is not list): return "Internal Model Error"
        return None


    def __EvaErrorsJObject(self):
        for Box in self.Boxes:
            errorJObject = self.__EvaErrorBox(Box)
            if (errorJObject != None):
                return errorJObject
        return None


    def __EvaErrorBox(self, Box: Box):
        errorHistoryCall = Box.EvaluateModelErrors()
        if (errorHistoryCall != None):
            return errorHistoryCall
        return None

