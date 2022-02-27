##
## EPITECH PROJECT, 2022
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
    def __init__(self, email: str, userName: str, customerInfos :CustomerInfos, localization :Localization):
        self.__InitJParent(email, userName)
        self.__InitJObject(customerInfos, localization)

    # Values Assignement
    def __InitJParent(self, email: str, userName: str):
        self.email = email
        self.userName = userName

    def __InitJObject(self, customerInfos :CustomerInfos, localization :Localization):
        self.CustomerInfos = customerInfos
        self.Localization = localization

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
        if (self.email is None): return "Internal server error"
        if (type(self.email) is not str): return "Internal server error"
        if (self.userName is None): return "Internal server error"
        if (type(self.userName) is not str): return "Internal server error"
        return None

    def __EvaCustomerInfosJObject(self):
        if (self.CustomerInfos is None): return "Internal server error"
        errorJObject = self.CustomerInfos.EvaErrorsJObject()
        if (errorJObject != None): "Internal server error"
        return None

    def __EvaLocalizationJObject(self):
        if (self.Localization is None): return "Internal server error"
        errorJObject = self.Localization.EvaErrorsJObject()
        if (errorJObject != None):return "Internal server error"
        return None

