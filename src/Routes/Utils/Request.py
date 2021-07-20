##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Request
##

# Validate the body of a request
def validateBody(json, keys):
    for i in keys:
        if not i in json:
            return False
    return True

