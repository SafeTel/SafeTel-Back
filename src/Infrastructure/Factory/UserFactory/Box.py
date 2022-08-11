##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Box
##

### INFRA
# Boxs db internal usage imports
import imp
from Infrastructure.Services.MongoDB.Balthasar.BoxDB import BoxDB
from Infrastructure.Services.MongoDB.Balthasar.UnclaimedBoxs import UnclaimedBoxsDB

### MODELS
# Box Model import
from Models.Infrastructure.Factory.UserFactory.Box.Box import Box
from Models.Infrastructure.Factory.UserFactory.Box.BoxList import BoxList
from Models.Infrastructure.Factory.UserFactory.Box.BoxSeverity import BoxSeverity
from Models.Logic.Shared.EmbeddedErrorReport import EmbeddedErrorReport

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
    def PullBoxes(self):
        return self.__PullBoxData()


    def PullBox(self, boxid: str):
        UserBoxes = self.__PullBoxData().Boxes
        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                return UserBox
        return None


    def IsBoxInCall(self, boxid: str):
        UserBox: Box = self.PullBox(boxid)
        return UserBox.call


    def IsClaimedByUser(self, boxid: str):
        UserBoxes = self.__PullBoxData().Boxes

        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                return True
        return False


    def IsRegisteredBoxIp(self, boxid: str, boxip: str):
        UserBoxes = self.__PullBoxData().Boxes

        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                if (self.__CheckBoxip(UserBox, boxip)):
                    return True
        return False


    # WRITE

    def ClaimBox(self, boxid: str):
        ClaimingBox = Box(boxid, False, "", True, BoxSeverity.NORMAL, [])

        if (not self.__UnclaimedBoxsDB.isValidBoxid(boxid)):
            return "This box isn't claimable"

        UserBoxes = self.__PullBoxData().Boxes

        for UserBox in UserBoxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                return "This box is already claimed by this account"

        self.__BoxDB.addBox(
            self.__guid,
            ClaimingBox.boxid,
            ClaimingBox.call,
            ClaimingBox.activity,
            BoxSeverity.EnumToStr(ClaimingBox.severity)
        )
        self.__UnclaimedBoxsDB.deleteByBoxid(boxid)

        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    def AddErrorReport(self, boxid: str, Error: EmbeddedErrorReport):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes.Boxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                self.__AddErrorReport(UserBox, Error)
                self.__BoxDB.updateBoxes(
                    self.__guid,
                    UserBoxes.ToDict()["Boxes"]
                )
                return None
        return "Unkwonw Box"


    def UpdateBoxIp(self, boxid: str, boxip: str):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes.Boxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                self.__ChangeBoxIp(UserBox, boxip)
                self.__BoxDB.updateBoxes(
                    self.__guid,
                    UserBoxes.ToDict()["Boxes"]
                )
                return None
        return "Unkwonw Box"


    def UpdateCall(self, boxid: str, call: bool):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes.Boxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                self.__ChangeCall(UserBox, call)
                self.__BoxDB.updateBoxes(
                    self.__guid,
                    UserBoxes.ToDict()["Boxes"]
                )
                return None
        return "Unkwonw Box"


    def UpdateActivity(self, boxid: str, activity: bool):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes.Boxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                self.__ChangeActivity(UserBox, activity)
                self.__BoxDB.updateBoxes(
                    self.__guid,
                    UserBoxes.ToDict()["Boxes"]
                )
                return None
        return "Unkwonw Box"


    def UpdateSeverity(self, boxid: str, severity: BoxSeverity):
        UserBoxes = self.__PullBoxData()

        for UserBox in UserBoxes.Boxes:
            if (self.__CheckBoxid(UserBox, boxid)):
                self.__ChangBoxMode(UserBox, severity)
                self.__BoxDB.updateBoxes(
                    self.__guid,
                    UserBoxes.ToDict()["Boxes"]
                )
                return None
        return "Unkwonw Box"


    # PRIVATE

    def __PullBoxData(self):
        return BoxList(self.__BoxDB.getBoxData(self.__guid)["Boxes"])


    def __CheckBoxid(self, UserBox: Box, boxid: str):
        return UserBox.boxid == boxid


    def __CheckBoxip(self, UserBox: Box, boxip: str):
        return UserBox.ip == boxip

    # UTILS

    def __ChangeBoxIp(self, UserBox: Box, boxip: str):
        UserBox.ip = boxip


    def __ChangeCall(self, UserBox: Box, call: bool):
        UserBox.call = call


    def __ChangeActivity(self, UserBox: Box, acitivity: bool):
        UserBox.activity = acitivity


    def __ChangBoxMode(self, UserBox: Box, severity: BoxSeverity):
        UserBox.severity = severity

    def __AddErrorReport(self, UserBox: Box, Error: EmbeddedErrorReport):
        UserBox.Reports.append(Error)
