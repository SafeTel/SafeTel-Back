##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## TellowsResponse
##
##

### MODELS
# Abstraction import
from Models.ModelAbstractions.JObject import JObject
# Shared Enum import
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity

# Represents Number Request
class TellowsResponseDTO(JObject):
    def __init__(self, loadedJSON: dict):
        self.__InitInputJObject(loadedJSON)

    def __init__(self, number: str, score: int, searches: str, comments: str, country: str):
        self.__InitOutputJObject(number, score, searches, comments, country)

    # Values Assignement
    def __InitInputJObject(self, loadedJSON: dict):
        self.number = self.LoadElement(loadedJSON, "number")
        self.score = int(self.LoadElement(loadedJSON, "score"))
        self.searches = int(self.LoadElement(loadedJSON, "searches"))
        self.comments = int(self.LoadElement(loadedJSON, "comments"))
        self.country = self.LoadElement(loadedJSON, "country")


    def __InitOutputJObject(self, number: str, score: int, searches: int, comments: int, country: str):
        self.number = number
        self.score = score
        self.searches = searches
        self.comments = comments
        self.country = country


    # Errors Evaluation
    def EvaluateModelErrors(self):
        errorJParent = self.__EvaErrorsJObject()
        if (errorJParent != None): return errorJParent
        return None


    def __EvaErrorsJObject(self):
        if (self.number is None): return "Model missing element - $number"
        if (type(self.number) is not str): return "Invalid variable type - $number"

        if (self.score is None): return "Model missing element - $score"
        if (type(self.score) is not int): return "Invalid variable type - $score"

        if (self.searches is None): return "Model missing element - $searches"
        if (type(self.searches) is not int): return "Invalid variable type - $searches"

        if (self.comments is None): return "Model missing element - $comments"
        if (type(self.comments) is not int): return "Invalid variable type - $comments"

        if (self.country is None): return "Model missing element - $country"
        if (type(self.country) is not str): return "Invalid variable type - $country"
        return None

