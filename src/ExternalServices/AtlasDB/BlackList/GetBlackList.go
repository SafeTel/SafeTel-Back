//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - GetBlackList.go
//

package blacklistCollection

import (
	"context"
	"log"

	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
	"go.mongodb.org/mongo-driver/bson" // Mongo Driver for bson data format
)

func (h *BlacklistHandler) GetBlacklistForUserId(userId string) models.ControlList {
	filter := bson.D{{Key: "userId", Value: userId}} // Filter to get userID elem
	var blackListPhoneNumbers models.ControlList     // Creating the list var PhoneNumber that will be filled with collection elems
	var content models.BlackListDataFormat

	if err := h.collection.FindOne(context.Background(), filter).Decode(&content); err != nil { // Get One elem from collection matching the filter option
		log.Panic(err)
	}

	log.Println("content: ", content)
	blackListPhoneNumbers.Number = content.PhoneNumbers // append elem to phoneNumbers list
	return blackListPhoneNumbers
}
