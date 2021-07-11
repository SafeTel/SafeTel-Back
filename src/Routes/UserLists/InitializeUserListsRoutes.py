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
from src.Routes.UserLists.BlackList.AddBlackList import AddBlackList
from src.Routes.UserLists.BlackList.DelBlackList import DelBlackList
from src.Routes.UserLists.BlackList.GetBlackList import GetBlackList
from src.Routes.UserLists.History.DelHistory import DelHistory
from src.Routes.UserLists.History.GetHistory import GetHistory
from src.Routes.UserLists.WhiteList.AddWhiteList import AddWhiteList
from src.Routes.UserLists.WhiteList.DelWhiteList import DelWhiteList
from src.Routes.UserLists.WhiteList.GetWhiteList import GetWhiteList
from src.Routes.UserLists.GreyList.GetGreyList import GetGreyList

def InitializeUserListsRoutes(api):
    api.add_resource(AddBlackList, "/user/blacklist")
    api.add_resource(DelBlackList, "/user/blacklist")
    api.add_resource(GetBlackList, "/user/blacklist")

    api.add_resource(GetHistory, "/user/history")
    api.add_resource(DelHistory, "/user/history")
    api.add_resource(AddWhiteList, "/user/whitelist")

    api.add_resource(DelWhiteList, "/user/whitelist")
    api.add_resource(GetWhiteList, "/user/whitelist")
    api.add_resource(GetGreyList, "/user/greylist")
