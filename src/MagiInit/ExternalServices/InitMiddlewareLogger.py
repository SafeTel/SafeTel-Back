##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Middleware Logger
##

### INFRA
# File for Logs
from Infrastructure.Utils.FileLogger.FileLogger import FileLogger
# Flask Request Import
from flask.globals import request as fquest

def MiddlewareLoggerForRequest():
    Logger = FileLogger.getInstance()

    buffer = EnvironInText(fquest)
    buffer += "\n\t- " + BodyRequestInText(fquest)

    Logger.Logger.info(buffer)

def EnvironInText(fquest):
    buffer = "Request Object:\n\tEnvironnement: "
    for i in fquest.environ:
        buffer += "\n\t- \"" + i + "\" = " + str(fquest.environ[i])
    return buffer

def BodyRequestInText(fquest):
    return "\"Body Request\" = " + str(fquest.args.to_dict())


def MiddlewareLoggerForResponses(response):
    Logger = FileLogger.getInstance()
    statusCode = response.status
    # Needed for the swagger to run to avoid errors
    response.direct_passthrough = False
    body = response.get_data(as_text=True)

    Logger.Logger.info("Response Object - Status Code " + statusCode + " :\n" + body)

    return response