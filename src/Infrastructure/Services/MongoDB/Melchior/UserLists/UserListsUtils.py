##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## MelchiorUtils
##

### INFRA
# Melchior DB imports
from Infrastructure.Services.MongoDB.Melchior.UserLists.BlackListDB import BlacklistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.WhiteListDB import WhitelistDB
from Infrastructure.Services.MongoDB.Melchior.UserLists.HistoryDB import HistoryDB

class UserListsUtils():
    def __inti__(self):
        self.BlacklistDb = BlacklistDB()
        self.WhitelistDb = WhitelistDB()
        self.HistoryDb = HistoryDB()


    # Create user lists for a guid
    def CreateUserLists(self, guid):
        self.BlacklistDb.newBlacklist(guid)
        self.WhitelistDb.newWhitelist(guid)
        self.HistoryDb.newHistory(guid)


    # Delete documents for the given user
    def DeleteUserLists(self, guid):
        self.BlacklistDb.deleteBlacklist(guid)
        self.WhitelistDb.deleteWhitelist(guid)
        self.HistoryDb.deleteHistory(guid)


    # Check if documents are deleted for the given user
    def IsDeletedUserLists(self, guid):
        if (not self.BlacklistDb.exists(guid)
        and not self.WhitelistDb.exists(guid)
        and not self.HistoryDb.exists(guid)):
            return True
        return False
