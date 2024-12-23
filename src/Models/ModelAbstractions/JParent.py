##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## JParent
##

### LOGIC
# json reader import
import json

# Represent a parent JSON Parent Object
class JParent():
    def Deserialize(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def ToDict(self):
        jsonRaw = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonRaw)

    def Load(self, rawJSON):
        if (type(rawJSON) is str): return json.loads(rawJSON)
        if (type(rawJSON) is dict): return rawJSON
        return None

    def LoadElement(self, loadedJSON: dict, key: str):
        return None if key not in loadedJSON else loadedJSON[key]
