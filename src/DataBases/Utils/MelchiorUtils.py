##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## MelchiorUtils
##

from DataBases.Melchior import BlacklistDB, WhitelistDB, HistoryDB

BlacklistDb = BlacklistDB()
WhitelistDb = WhitelistDB()
HistoryDb = HistoryDB()

def createDocumentForNewUser(guid):
    BlacklistDb.newBlacklist(guid)
    WhitelistDb.newWhitelist(guid)
    HistoryDb.newHistory(guid)
