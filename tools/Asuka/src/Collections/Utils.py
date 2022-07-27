##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Balthasar
##

### LOGIC
# For Getenv
import logging
import os

### INFRA
# Mongo Collection
import pymongo
# Callable import for annotation function as argument
from typing import Callable


import json
from bson import json_util

## Util Function for Collection
#
#   Launch Func while getting collection content 
#
def GetCollectionContentAndFunc(collection: pymongo.collection, func: Callable[[list], bool], DocumentsMaxIterationNumber = 5000000000, DocumentsPageSize = 50):
    for i in range(DocumentsMaxIterationNumber): 
        RangeMin = i * DocumentsPageSize
        RangeMax = DocumentsPageSize + RangeMin

        DocumentsWithPaging = collection.find().skip(RangeMin).limit(RangeMax)

        func(DocumentsWithPaging)

        DocumentsWithPagingInList = list(DocumentsWithPaging)
        if (DocumentsWithPagingInList.__len__() == 0):
            break