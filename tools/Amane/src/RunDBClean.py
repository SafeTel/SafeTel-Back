##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# Run Clean 
##

### INFRA
# Client mongo db import
import pymongo

### LOGIC
# env var import
import os
# Schedule events using hours
from datetime import datetime, timezone
# Sleep
import time
# Thread in python
import threading

from DBClean import DBClean

def runDBClean(argv):
    Client = pymongo.MongoClient(os.getenv("DB_URI"))

    MongoDBClean = DBClean(Client)
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_MELCHIOR"), ['Blacklist', 'History', 'User', 'Whitelist'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_CASPER"), ['ApiKeyLog', 'Contributors'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_CASPER_02"), ['GoogleServices'])
    MongoDBClean.setDatabasesCollectionPair(os.getenv("DB_BALTHASAR"), ['Boxes', 'UnclaimedBoxes'])

    if (len(argv) == 2):
        if (argv[1] == '--force-now'):
            MongoDBClean.run()
            return 0

    isCleanLaunched = 0
    while True:
        currentTime = datetime.now(tz=timezone.utc).time()
        hour = currentTime.hour
        minute = currentTime.minute

        if (10 <= hour < 11):
            if (20 < minute < 30 and isCleanLaunched == 0):
                threadPerformingCleaning = threading.Thread(target=MongoDBClean.run())
                threadPerformingCleaning.start()
                threadPerformingCleaning.join()
                isCleanLaunched = 1
        else:
                isCleanLaunched = 0
        # 5 minutes Sleep
        time.sleep(300)