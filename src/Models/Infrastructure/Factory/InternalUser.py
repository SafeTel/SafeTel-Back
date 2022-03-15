
### MODELS
# Abstraction import
from Models.ModelAbstractions.JParent import JParent
# Roles enum import
from Models.Logic.Shared.Roles import Roles
# Shared JObject imports
from Models.Endpoints.SharedJObject.Account.Infos.CustomerInfos import CustomerInfos
from Models.Endpoints.SharedJObject.Account.Infos.Localization import Localization
from Models.Endpoints.SharedJObject.Account.Infos.Administrative import Administrative

### LOGIC
# time import
import time

# Represents InternalUser
class InternalUser(JParent):
    def __init__(self, rawJSON: str, guid: str, password: str):
        loadedJSON = self.Load(rawJSON)
        self.__InitJParent(loadedJSON, guid, password)
        self.__InitCustomerInfosJObject(loadedJSON)
        self.__InitLocalizationJObject(loadedJSON)
        self.__InitAdministrativeJObject()

    # Values Assignement
    def __InitJParent(self, loadedJSON: dict, guid: str, password: str):
        self.email = self.LoadElement(loadedJSON, "email")
        self.username = self.LoadElement(loadedJSON, "username")
        self.password = password
        self.time = time.time()
        self.guid = guid
        self.role = Roles.USER

    def __InitCustomerInfosJObject(self, loadedJSON: dict):
        customerInfosRaw = self.LoadElement(loadedJSON, "CustomerInfos")
        self.CustomerInfos = None if customerInfosRaw is None else CustomerInfos(customerInfosRaw)

    def __InitLocalizationJObject(self, loadedJSON: dict):
        localizationRaw = self.LoadElement(loadedJSON, "Localization")
        self.Localization = None if localizationRaw is None else Localization(localizationRaw)

    def __InitAdministrativeJObject(self):
        self.Administrative = Administrative()

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
        if (self.email is None): return "Body Denied"
        if (type(self.email) is not str): return "Email Denied"
        if (self.username is None): return "Body Denied"
        if (type(self.username) is not str): return "Username Denied"
        if (self.password is None): return "Passwor Denied"
        if (type(self.password) is not str): return "Body Denied"
        if (self.time is None): return "Time Denied"
        if (type(self.time) is not float): return "Body Denied"
        if (self.guid is None): return "GUID Denied"
        if (type(self.guid) is not str): return "Body Denied"
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
