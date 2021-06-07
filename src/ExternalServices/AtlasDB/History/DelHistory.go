//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - DelHistory.go
//

package historyCollections

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/bson" // Mongo Driver for bson data format
)

func (h *HistoryHandler) DelHistoryCallForUserId(userId string, number string, unixTimeStamp int) {
	filter := bson.D{{Key: "userId", Value: userId}}
	update := bson.D{
		{Key: "$pull", Value: bson.D{ // $pull remove an elem that will match the Value:
			{Key: "history", Value: bson.D{
				{Key: "number", Value: number},
				{Key: "time", Value: unixTimeStamp},
			},
			},
		},
		},
	} // Want to $push(add) Value into phoneNumbers field
	deleteResult, err := h.collection.UpdateOne(context.Background(), filter, update)

	if err != nil { // Get One elem from collection matching the filter option
		log.Panic(err)
	}
	log.Println("Blacklist DeleteOne Result: number of elem modified: ", deleteResult.ModifiedCount)
}
