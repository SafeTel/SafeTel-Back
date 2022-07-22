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

def GetCollectionContentAndFunc(collection: pymongo.collection, func: Callable[[list], bool], DocumentsMaxIterationNumber = 5000000000, DocumentsPageSize = 50):
    logging.info("GetCollectionContentAndFunc")

    for i in range(DocumentsMaxIterationNumber): 
        RangeMin = i * DocumentsPageSize
        RangeMax = DocumentsPageSize + RangeMin
        BoxesDocumentsWithPagingInList = list(collection.find().skip(RangeMin).limit(RangeMax))

        if len(list(BoxesDocumentsWithPagingInList)) <= 0:
            break

    func(BoxesDocumentsWithPagingInList)