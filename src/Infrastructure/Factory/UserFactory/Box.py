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
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity


### /!\ WARNING /!\ ###
# This is an HIGH LEVEL User INFRA interface including logic, proceed with caution
### /!\ WARNING /!\ ###


# Class to represents the usage of a Box inside the server (Worker)
class FactBox():
    def __init__(self, guid: str):
        self.__guid = guid

        self.__BoxDB = BoxDB()
        self.__UnclaimedBoxsDB = UnclaimedBoxsDB()


    # READ
    def PullBoxData(self):
        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    # WRITE
    def ClaimBox(self, boxid: str):
        ClaimingBox = Box(boxid, True, BoxSeverity.NORMAL)

        if (not self.__UnclaimedBoxsDB.isValidBoxid(boxid)):
            return "This box isn't claimable"

        UserBoxes = self.__PullBoxData().Boxes

        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                return "This box is already claimed by this account"

        self.__BoxDB.addBox(
            self.__guid,
            ClaimingBox.boxid,
            ClaimingBox.activity,
            BoxSeverity.EnumToStr(ClaimingBox.severity)
        )
        self.__UnclaimedBoxsDB.deleteByBoxid(boxid)

        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    def IsClaimedByUser(self, boxid: str):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                return True
        return False


    # PRIVATE
    def __PullBoxData(self):
        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    def __CheckBoxid(self, UserBox: Box, boxid: str):
        return UserBox.boxid == boxid
