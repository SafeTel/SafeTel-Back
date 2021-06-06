//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - blackListDB.go
//

package atlasCollections

import (
	"context"
	"log"

	"github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"
	"go.mongodb.org/mongo-driver/mongo"
	"gopkg.in/mgo.v2/bson"
)

// ./src/DB/BlackListDB.go de:
// - D'obtenir la liste des utilisateurs BlackListés à partir de l'id d'un utilisateur
// GetBlackList(userId string)

// - De WhiteLister un numéro  à partir d'un numéro à BlackList et de l'id de l'utilisateur
// BlackListNumber(userId string, number string)

// - D'enlever un numéro de la BlackList à partir d'un numéro à BlackList et de l'id de l'utilisateur
// UNBlackListNumber(userId string, number string)

type BlacklistHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func (h *BlacklistHandler) GetBlacklistForUserId(userId string) []dataModels.PhoneNumber {
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

func (h *BlacklistHandler) AddBlacklistPhoneNumberForUserId(userId string, phoneNumber dataModels.PhoneNumber) {
	filter := bson.M{"userId": userId}                                                // Filter to get userID elem
	update := bson.M{"phoneNumbers": bson.M{"$push": phoneNumber.Value}}              // Want to $push(add) Value into phoneNumbers field
	updateResult, err := h.collection.UpdateOne(context.Background(), filter, update) // proceed update into filter result

	if err != nil {
		log.Panic("Blacklist UpdateOne() ERROR:", err)
	}
	log.Println("Blacklist UpdateOne Result:", updateResult)
}

func (h *BlacklistHandler) DeleteBlacklistPhoneNumberForUserId(userId string, phoneNumber dataModels.PhoneNumber) {
	filter := bson.M{
		"userId":       userId,
		"phoneNumbers": bson.M{"$eq": userId},
	} // Create a filter to match conditions
	deleteResult, err := h.collection.DeleteOne(context.Background(), filter)

	if err != nil {
		log.Panic("DeleteOne() ERROR:", err)
	}
	log.Println("Blacklist DeleteOne Result:", deleteResult)
}

func NewBlacklist(client *mongo.Client, dbName string) *BlacklistHandler {
	object := BlacklistHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("Blacklist"),
	}
	return &object
}
