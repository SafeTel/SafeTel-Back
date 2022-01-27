##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeUserListsRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.UserLists.BlackList.AddBlackList import AddBlackList
from Routes.UserLists.BlackList.DelBlackList import DelBlackList
from Routes.UserLists.BlackList.GetBlackList import GetBlackList
from Routes.UserLists.History.AddHistory import AddHistory
from Routes.UserLists.History.DelHistory import DelHistory
from Routes.UserLists.History.GetHistory import GetHistory
from Routes.UserLists.WhiteList.AddWhiteList import AddWhiteList
from Routes.UserLists.WhiteList.DelWhiteList import DelWhiteList
from Routes.UserLists.WhiteList.GetWhiteList import GetWhiteList
from Routes.UserLists.GreyList.GetGreyList import GetGreyList

def InitializeUserListsRoutes(api):
    api.add_resource(AddBlackList, "/user/blacklist")
    api.add_resource(DelBlackList, "/user/blacklist")
    api.add_resource(GetBlackList, "/user/blacklist")

    api.add_resource(AddHistory, "/user/history")
    api.add_resource(DelHistory, "/user/history")
    api.add_resource(GetHistory, "/user/history")

    api.add_resource(AddWhiteList, "/user/whitelist")
    api.add_resource(DelWhiteList, "/user/whitelist")
    api.add_resource(GetWhiteList, "/user/whitelist")

    api.add_resource(GetGreyList, "/user/greylist")
