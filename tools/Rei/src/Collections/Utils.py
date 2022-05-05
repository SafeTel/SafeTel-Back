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


def CopyAndUpload(FromCollectionToCopy, ToCollection, DocumentsMaxIterationNumber = 5000000000, DocumentsPageSize = 50):
    # Using i for paging datas -> avoiding the use of to much memory at the same time
    for i in range(DocumentsMaxIterationNumber): 
        RangeMin = i * DocumentsPageSize
        RangeMax = DocumentsPageSize + RangeMin
        BoxesDocumentsWithPagingInList = list(FromCollectionToCopy.find().skip(RangeMin).limit(RangeMax))
            
        if len(list(BoxesDocumentsWithPagingInList)) <= 0:
            break
        ToCollection.insert_many(list(BoxesDocumentsWithPagingInList))
