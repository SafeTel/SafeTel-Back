##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## script
##

from cmath import log
import logging
import sys
import hashlib

format = "%(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def logHelp():
    logging.info("Password encryption in the format:")
    logging.info("\t<PYTHON_INTERPRETER> script.py <PASSWORD>")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'input "PostmanDbDataImplementation/errors"':
            logHelp()
            sys.exit(1)
        password = sys.argv[1]
        logging.info('You are going to hash the password: \'' + password + '\' using SHA 3 in 512 bytes')
        logging.info('Processing...')
        logging.info('hashing the password...')
        hash_sha3_512 = hashlib.new("sha3_512", password.encode())
        logging.info('Done!')
        logging.info('Your hashed password is:')
        logging.info(hash_sha3_512.hexdigest())
    else:
        logging.warning('Error: Wrong number of argument: ')
        logHelp()
        sys.exit(1)
    sys.exit(0)
