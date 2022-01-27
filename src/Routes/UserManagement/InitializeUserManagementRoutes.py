##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## InitializeUserManagementRoutes
##

# Network Imports
import requests
from flask import Flask
from flask_restful import Api

# Endpoints imports
from Routes.UserManagement.Register import Register
from Routes.UserManagement.Login import Login
from Routes.UserManagement.DeleteAccount import DeleteAccount
from Routes.UserManagement.UpdateEmail import UpdateEmail
from Routes.UserManagement.ChangePersonalInfos import ChangesPersonalInfos

def InitializeUserManagementRoutes(api):
    api.add_resource(Register, "/user/register")
    api.add_resource(Login, "/user/login")
    api.add_resource(DeleteAccount, "/user/deleteAccount")
    api.add_resource(UpdateEmail, "/user/updateEmail")
    api.add_resource(ChangesPersonalInfos, "/user/changePersonalInfos")
