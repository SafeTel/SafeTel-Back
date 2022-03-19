##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Box
##

### INFRA
# Boxs db internal usage imports
from Infrastructure.Services.MongoDB.Balthasar.Box import BoxDB
from Infrastructure.Services.MongoDB.Balthasar.UnclaimedBoxs import UnclaimedBoxsDB

### MODELS


### /!\ WARNING /!\ ###
# This is an HIGH LEVEL User INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Class to represents the usage of a user inside the server (Worker)
class Box():
    def __init__(self, guid: str):
        self.__guid = guid

        self.__BoxDB = BoxDB()
        self.__UnclaimedBoxsDB = UnclaimedBoxsDB()


    # READ
    def PullBoxData(self):
        return self.__BoxDB.getBoxData() # must return model


    # WRITE
    def ClaimBox(self, boxid):
        box = 0 # init the unique box model
        # looks if there is already a box for this user
            # yes -> addbox
        self.__BoxDB.addBox(box)
            # no -> init the whole model
        self.__BoxDB.createDataBox(box)

        self.__UnclaimedBoxsDB.deleteByBoxid(boxid)
