##
## SAFETEL PROJECT, 2021
## SafeTel-Back
## File description:
## Types
##

# import re for regular expression matching
import re

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Validate as a valid phone number
def isValidNumber(data):
    if (len(data) != 10):
        return False
    return data.isnumeric()

# Validate a string as a valid email
def isValidEmail(data):
    return re.match(emailRegex, data)
