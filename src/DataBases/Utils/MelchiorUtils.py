##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## MelchiorUtils
##

# Melchior DB imports
from DataBases.Melchior.BlackListDB import BlacklistDB
from DataBases.Melchior.WhiteListDB import WhitelistDB
from DataBases.Melchior.HistoryDB import HistoryDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()
HistoryDb = HistoryDB()

# Create user lists for a guid
def createDocumentForNewUser(guid):
    BlacklistDb.newBlacklist(guid)
    WhitelistDb.newWhitelist(guid)
    HistoryDb.newHistory(guid)

# Delete documents for the given user
def deleteDocumentForUser(guid):
    BlacklistDb.deleteBlacklist(guid)
    WhitelistDb.deleteWhitelist(guid)
    HistoryDb.deleteHistory(guid)

# Check if documents are deleted for the given user
def isDeletedDocumentForUser(guid):
    if (not BlacklistDb.exists(guid)
    and not WhitelistDb.exists(guid)
    and not HistoryDb.exists(guid)):
        return True
    return False
