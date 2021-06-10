//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - DelBlackList.go
//

package blacklistCollection

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/bson" // Mongo Driver for bson data format
)

func (h *BlacklistHandler) DelBlacklistPhoneNumberForUserId(userId string, phoneNumber string) {
	filter := bson.D{{Key: "userId", Value: userId}}
	update := bson.D{
		{Key: "$pull", Value: bson.D{ // $pull remove an elem that will match the Value:
			{Key: "phoneNumbers", Value: phoneNumber}},
		},
	} // Want to $push(add) Value into phoneNumbers field
	deleteResult, err := h.collection.UpdateOne(context.Background(), filter, update)

	if err != nil {
		log.Panic("DeleteOne() ERROR:", err)
	}
	log.Println("Blacklist DeleteOne Result: number of elem modified: ", deleteResult.ModifiedCount)
}
