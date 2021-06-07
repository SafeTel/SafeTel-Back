//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - AddBlackList.go
//

package blacklistCollection

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/bson" // Mongo Driver for bson data format
)

func (h *BlacklistHandler) AddBlacklistPhoneNumberForUserId(userId string, number string) {
	filter := bson.D{{Key: "userId", Value: userId}} // Filter to get userID elem
	update := bson.D{
		{Key: "$push", Value: bson.D{
			{Key: "phoneNumbers", Value: number}},
		},
	} // Want to $push(add) Value into phoneNumbers field
	updateResult, err := h.collection.UpdateOne(context.Background(), filter, update) // proceed update into filter result

	if err != nil {
		log.Panic("Blacklist UpdateOne() ERROR:", err)
	}

	log.Println("Blacklist UpdateOne Result:", updateResult)
}
