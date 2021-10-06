##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## AvaibleUpdate
##

# Network imports
from flask import request as fquest
from flask_restful import Resource
import random

# Utils check imports
from Routes.Utils.Request import validateBody

def EAvaibleUpdate(data):
    if not validateBody(
        data,
        ["magicNumber", "version"]):
        return False
    if data["magicNumber"] != 42:
        return False
    return True

# Route to know if an update is required for the embeded software
class AvaiableUpdate(Resource):
    def post(self):
        body = fquest.get_json()

        if not EAvaibleUpdate(body):
            return {
                'error': 'bad_request'
            }, 400

        version = body["version"]

        """if self.isReleaseVersion(version):
            return {
                'error': 'not a release version'
            }, 400 """

        if version != "1.0":
            return {
                'update': False
            }

        return {
            'update': True
        }

    def isReleaseVersion(self, version): # TODO: verify release from tags on github with version std
        return not version == "1.0"
