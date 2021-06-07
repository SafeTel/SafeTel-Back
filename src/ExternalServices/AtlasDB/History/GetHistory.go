//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - GetHistory.go
//

package historyCollections

import (
	"context"
	"log"

	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
	"go.mongodb.org/mongo-driver/bson" // Mongo Driver for bson data format
)

func (h *HistoryHandler) GetHistoryForUserId(userId string) []models.Call {
	filter := bson.D{{Key: "userId", Value: userId}} // Filter to get userID elem
	var content models.History                       // Var that will be fill with history content
	var historyCalls []models.Call

	if err := h.collection.FindOne(context.Background(), filter).Decode(&content); err != nil { // Get One elem from collection matching the filter option
		log.Panic(err)
	}

	for _, elem := range content.Values {
		var newCall models.Call
		newCall.Number = elem.Number
		newCall.Origin = elem.Origin
		newCall.Time = elem.Time
		historyCalls = append(historyCalls, newCall)
	}

	return historyCalls
}
