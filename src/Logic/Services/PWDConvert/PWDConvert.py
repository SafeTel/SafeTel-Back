##
## EPITECH PROJECT, 2021
## SafeTel-Back
## File description:
## Serializer
##

### LOGIC
# sha3 imports
import sys
import hashlib

class PWDConvert():
    def __init__(self):
        # inferior system version import
        if sys.version_info < (3, 6):
           import sha3


    def Serialize(slef, pwd):
        hash_sha3_512 = hashlib.new("sha3_512", pwd.encode())
        return hash_sha3_512.hexdigest()


    def Compare(self, plain_pwd, hashed_pwd):
        hash_sha3_512 = hashlib.new("sha3_512", plain_pwd.encode())
        plain_hashed_pwd = hash_sha3_512.hexdigest()

        if (plain_hashed_pwd == hashed_pwd):
            return True
        return False
