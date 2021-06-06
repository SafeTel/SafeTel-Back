//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - atlasWhitelistCollection.go
//

package atlasCollections

import (
	"context"
	"log"

	dataModels "github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"
	"go.mongodb.org/mongo-driver/mongo"
	"gopkg.in/mgo.v2/bson"
)

type WhitelistHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func (h *WhitelistHandler) GetWhiteListForUserId(userId string) []dataModels.PhoneNumber {
	filter := bson.M{"userId": userId}                             // Filter to get userID elem
	cursor, err := h.collection.Find(context.Background(), filter) // Get all elems from collection matching the filter option

	if err != nil {
		log.Panic(err)
	}
	defer cursor.Close(context.Background())  // Defering the close of the cursor. Work like the closing of an IO
	var phoneNumbers []dataModels.PhoneNumber // Creating the list var PhoneNumber that will be filled with collection elems

	for cursor.Next(context.Background()) { // Iterating on all elems of the cursor
		var elem dataModels.PhoneNumber // Var that will be fill with the current value of the cursor
		err := cursor.Decode(&elem)     // Decode the cursor value and fill the elem var

		if err != nil {
			log.Panic(err)
		}
		phoneNumbers = append(phoneNumbers, elem) // append elem to phoneNumbers list
	}
	return phoneNumbers
}

func (h *WhitelistHandler) AddWhiteListPhoneNumberForUserId(userId string, phoneNumber dataModels.PhoneNumber) {
	filter := bson.M{"userId": userId}                                                // Filter to get userID elem
	update := bson.M{"phoneNumbers": bson.M{"$push": phoneNumber.Value}}              // Want to $push(add) Value into phoneNumbers field
	updateResult, err := h.collection.UpdateOne(context.Background(), filter, update) // proceed update into filter result

	if err != nil {
		log.Panic("Whilelist UpdateOne() ERROR:", err)
	}
	log.Println("Whilelist UpdateOne Result:", updateResult)
}

func (h *WhitelistHandler) DeleteWhiteListPhoneNumberForUserId(userId string, phoneNumber dataModels.PhoneNumber) {
	filter := bson.M{
		"userId":       userId,
		"phoneNumbers": bson.M{"$eq": userId},
	} // Create a filter to match conditions
	deleteResult, err := h.collection.DeleteOne(context.Background(), filter)

	if err != nil {
		log.Panic("DeleteOne() ERROR:", err)
	}
	log.Println("Whilelist DeleteOne Result:", deleteResult)
}

func NewWhilelist(client *mongo.Client, dbName string) *WhitelistHandler {
	object := WhitelistHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("Whitelist"),
	}
	return &object
}
