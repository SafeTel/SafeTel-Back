##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## JWTEmbeddedInfos
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents Update Email Response
class JWTInfos(JParent):
    def __init__(self, guid: str, boxid: str, exp: int):
        self.__InitJParent(guid, boxid, exp)

    # Values Assignement
    def __InitJParent(self, guid: str, boxid: str, exp: int):
        self.guid = guid
        self.boxid = boxid
        self.exp = exp

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.guid is None): return "guid is undefined"
        if (type(self.guid) is not str): return "guid invalid variable type"

        if (self.boxid is None): return "boxid is undefined"
        if (type(self.boxid) is not str): return "boxid invalid variable type"

        if (self.exp is None): return "exp is undefined"
        if (type(self.exp) is not int): return "exp invalid variable type"
        return None
