##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## MelchiorUtils
##

# Melchior DB imports
from DataBases.Melchior import BlacklistDB, WhitelistDB, HistoryDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()
HistoryDb = HistoryDB()

# Create user lists for a guid
def createDocumentForNewUser(guid):
    BlacklistDb.newBlacklist(guid)
    WhitelistDb.newWhitelist(guid)
    HistoryDb.newHistory(guid)
