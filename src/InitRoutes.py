##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## launchingRoutes
##

### LOGIC
import logging

### INFRA
# User Routes
from Routes.UserManagement.InitializeUserManagementRoutes import InitializeUserManagementRoutes
from Routes.UserLists.InitializeUserListsRoutes import InitializeUserListsRoutes
# Initialize s Routes
from Routes.Services.InitializeServicesRoutes import InitializeServicesRoutes
# Initialize server ressources routes
from Routes.ServerManagement.InitializeServerManagementRoutes import InitializeServerManagementRoutes
# Initialize embeded ressources routes
from Routes.EmbededRessources.InitializeEmbededRessourcesRoutes import InitializeEmbededRessourceRoutes
# Initialize dev ressources routes
from Routes.DevRessources.InitializeDevRessources import InitializeDevRessourcesRoutes

def InitRoutes(api):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    InitializeUserManagementRoutes(api)
    logging.info("Routes initialized - User Management")

    InitializeUserListsRoutes(api)
    logging.info("Routes initialized - User Lists")

    InitializeServicesRoutes(api)
    logging.info("Routes initialized - Services")

    InitializeServerManagementRoutes(api)
    logging.info("Routes initialized - Server Management")

    InitializeEmbededRessourceRoutes(api)
    logging.info("Routes initialized - Embeded Ressources")

    InitializeDevRessourcesRoutes(api)
    logging.info("Routes initialized - Dev Ressources")
