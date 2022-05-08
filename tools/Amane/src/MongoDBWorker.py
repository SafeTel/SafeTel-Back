##
# SAFETEL PROJECT, 2022
# SafeTel-Back
# File description:
# DataWorker
##

# INFRA
# Client mongo db import
from typing import Any
import pymongo

# Delete multiple documents
def DeleteManyDocument(db, query: Any):
    if query == None:
        return
    db.delete_many(query)
