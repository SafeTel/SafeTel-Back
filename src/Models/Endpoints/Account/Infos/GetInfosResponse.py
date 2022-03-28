##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## GetInfosResponse
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared JObject import
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

# Represents UpdatePErsonalInfos Request
class GetInfosResponse(JParent):
    def __init__(self, email: str, username: str, CustomerInfos :CustomerInfos, Localization :Localization):
        self.__InitJParent(email, username)
        self.__InitJObject(CustomerInfos, Localization)

    # Values Assignement
    def __InitJParent(self, email: str, username: str):
        self.email = email
        self.username = username

    def __InitJObject(self, CustomerInfos :CustomerInfos, Localization :Localization):
        self.CustomerInfos = CustomerInfos
        self.Localization = Localization

    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJParent()
        if (errorJParent != None): return errorJParent
        errorJObject = self.__EvaCustomerInfosJObject()
        if (errorJObject != None): return errorJObject
        errorJObject = self.__EvaLocalizationJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaErrorsJParent(self):
        if (self.email is None): return "Internal Model Error"
        if (type(self.email) is not str): return "Internal Model Error"
        if (self.username is None): return "Internal Model Error"
        if (type(self.username) is not str): return "Internal Model Error"
        return None

    def __EvaCustomerInfosJObject(self):
        if (self.CustomerInfos is None): return "Internal Model Error"
        errorJObject = self.CustomerInfos.EvaErrorsJObject()
        if (errorJObject != None): "Internal Model Error"
        return None

    def __EvaLocalizationJObject(self):
        if (self.Localization is None): return "Internal Model Error"
        errorJObject = self.Localization.EvaErrorsJObject()
        if (errorJObject != None):return "Internal Model Error"
        return None

