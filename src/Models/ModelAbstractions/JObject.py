##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## JObject
##

### LOGIC
# json reader import
import json

# Represent a parent JSON Object
class JObject():
    def Deserialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def LoadElement(self, loadedJSON: dict, key: str):
        return None if key not in loadedJSON else loadedJSON[key]
