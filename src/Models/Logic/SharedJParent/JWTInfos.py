##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## JWTInfos
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared Logic model import
from Models.Logic.Shared.Roles import Roles

# Represents Update Email Response
class JWTInfos(JParent):
    def __init__(self, guid: str, role: Roles, exp: int):
        self.__InitJParent(guid, role, exp)

    # Values Assignement
    def __InitJParent(self, guid: str, role: Roles, exp: int):
        self.guid = guid
        self.role = role
        self.exp = exp

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.guid is None): return "guid is undefined"
        if (type(self.guid) is not str): return "guid invalid variable type"
        if (self.role is None): return "role is undefined"
        if (type(self.role) is not Roles and not Roles.HasValue(self.role)): return "role invalid variable type"
        if (self.exp is None): return "exp is undefined"
        if (type(self.exp) is not int): return "exp invalid variable type"
        return None
