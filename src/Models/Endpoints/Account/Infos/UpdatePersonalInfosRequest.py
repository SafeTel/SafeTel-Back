##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## UpdatePersonalInfos.Request
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Shared JObject import
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization

# Represents UpdatePErsonalInfos Request
class UpdatePErsonalInfosRequest(JParent):
    def __init__(self, rawJSON: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON)
        self.__InitCustomerInfosJObject(loadedJSON)
        self.__InitLocalizationJObject(loadedJSON)

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict):
        self.token = self.LoadElement(loadedJSON, "token")

    def __InitCustomerInfosJObject(self, loadedJSON: dict):
        customerInfosRaw = self.LoadElement(loadedJSON, "CustomerInfos")
        self.CustomerInfos = None if customerInfosRaw is None else CustomerInfos(customerInfosRaw)

    def __InitLocalizationJObject(self, loadedJSON: dict):
        localizationRaw = self.LoadElement(loadedJSON, "Localization")
        self.Localization = None if localizationRaw is None else Localization(localizationRaw)

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
        if (self.token is None): return "Body Denied"
        if (type(self.token) is not str): return "Token Denied"
        return None

    def __EvaCustomerInfosJObject(self):
        if (self.CustomerInfos is None): return "Body Denied"
        errorJObject = self.CustomerInfos.EvaErrorsJObject()
        if (errorJObject != None): return errorJObject
        return None

    def __EvaLocalizationJObject(self):
        if (self.Localization is None): return "Body Denied"
        errorJObject = self.Localization.EvaErrorsJObject()
        if (errorJObject != None):return errorJObject
        return None
