##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Box
##

### INFRA
# Boxs db internal usage imports
from Infrastructure.Services.MongoDB.Balthasar.BoxDB import BoxDB
from Infrastructure.Services.MongoDB.Balthasar.UnclaimedBoxs import UnclaimedBoxsDB

### MODELS
# Box Model import
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
from Models.Infrastructure.Factory.UserFactory.Box.BoxList import BoxList


### /!\ WARNING /!\ ###
# This is an HIGH LEVEL User INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Class to represents the usage of a user inside the server (Worker)
class FactBox():
    def __init__(self, guid: str):
        self.__guid = guid

        self.__BoxDB = BoxDB()
        self.__UnclaimedBoxsDB = UnclaimedBoxsDB()


    # READ
    def PullBoxData(self):
        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    # WRITE
    def ClaimBox(self, boxid):
        box = 0 # init the unique box model
        # looks if there is already a box for this user
            # yes -> addbox
        self.__BoxDB.addBox(box)
            # no -> init the whole model
        self.__BoxDB.createDataBox(box)

        self.__UnclaimedBoxsDB.deleteByBoxid(boxid)

        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])
