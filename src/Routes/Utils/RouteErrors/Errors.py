##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Errors
##

def InternalLogicError():
    return {
        'error': True,
        'details': 'internal logic error'
    }

def BadRequestError(details):
    return {
        'error': True,
        'details':details
    }, 400
