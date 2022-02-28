##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## AvaibleUpdate
##

# Network imports
from flask import request as fquest
from flask_restful import Resource

# Request Error
from Endpoints.Utils.RouteErrors.Errors import BadRequestError, InternalLogicError

from Models.Endpoints.InternalDev.Embeded.AvaibleUpdateRequest import AvaibleUpdateRequest
from Models.Endpoints.InternalDev.Embeded.AvaibleUpdateResponse import AvaibleUpdateResponse

# Route to know if an update is required for the embeded software
class AvaiableUpdate(Resource):
    def post(self):
        Request = AvaibleUpdateRequest(fquest.get_json())

        requestErrors = Request.EvaluateModelErrors()
        if (requestErrors != None):
            return BadRequestError(requestErrors), 400

        Response = AvaibleUpdateResponse(Request.version == 1.0)

        responseErrors = Response.EvaluateModelErrors()
        if (responseErrors != None):
            return InternalLogicError(), 500
        return Response.ToDict(), 200
