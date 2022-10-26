##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# Run Save
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

from SaveDatabases import SaveDatabases

def runDBSave(argv):
    if (len(argv) == 2):
        if (argv[1] == '--force-now'):
            SaveDatabases()
            return 0

    isCleanLaunched = 0
    while True:
        currentTime = datetime.now(tz=timezone.utc).time()

        if (8 <= currentTime.hour < 9):
            if (20 < currentTime.minute < 30 and isCleanLaunched == 0):
                SaveDatabases()
                isCleanLaunched = 1
        else:
                isCleanLaunched = 0
        # 5 minutes Sleep
        time.sleep(300)
