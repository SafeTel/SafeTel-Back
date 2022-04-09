##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## DeleteAccount.Response
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent

# Represents DeleteAccount Request
class DeleteAccountResponse(JParent):
    def __init__(self, deleted: bool):
        self.__InitJParent(deleted)

    # Values Assignement
    def __InitJParent(self, deleted: bool):
        self.deleted = deleted

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        return None

    def __EvaErrorsJParent(self):
        if (self.deleted is None): return "Internal Model Error"
        if (type(self.deleted) is not bool): return "Internal Model Error"
        return None
