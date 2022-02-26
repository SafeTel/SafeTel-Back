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
from Endpoints.UserManagement.InitializeUserManagementRoutes import InitializeUserManagementRoutes
from Endpoints.UserLists.InitializeUserListsRoutes import InitializeUserListsRoutes
# Initialize s Routes
from Endpoints.Services.InitializeServicesRoutes import InitializeServicesRoutes
# Initialize server ressources routes
from Endpoints.ServerManagement.InitializeServerManagementRoutes import InitializeServerManagementRoutes
# Initialize embeded ressources routes
from Endpoints.EmbededRessources.InitializeEmbededRessourcesRoutes import InitializeEmbededRessourceRoutes
# Initialize dev ressources routes
from Endpoints.DevRessources.InitializeDevRessources import InitializeDevRessourcesRoutes

def InitEndpoints(api):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Routes initialization...")

    InitializeUserManagementRoutes(api)
    logging.info("- User Management")

    InitializeUserListsRoutes(api)
    logging.info("- User Lists")

    InitializeServicesRoutes(api)
    logging.info("- Services")

    InitializeServerManagementRoutes(api)
    logging.info("- Server Management")

    InitializeEmbededRessourceRoutes(api)
    logging.info("- Embeded Ressources")

    InitializeDevRessourcesRoutes(api)
    logging.info("- Dev Ressources")
