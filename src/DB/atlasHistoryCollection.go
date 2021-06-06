//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - historyDB.go
//

package atlasCollections

import (
	"context"
	"log"

	"github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"
	"go.mongodb.org/mongo-driver/mongo"
	"gopkg.in/mgo.v2/bson"
)

// ./src/DB/HistoryDB.go de:
// - D'obtenir l'history à partir de l'id d'un utilisateur
// GetHistory(userId string)

// - D'enlever un appel de l'history à partir d'un numéro, d'un timestamp unix, et de l'id de l'utilisateur
// UNBlackListNumber(userId string, number string, unixtimestamp int)

type HistoryHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func (h *HistoryHandler) GetHistoryForUserId(userId string) []dataModels.PhoneNumber {
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

func NewHistory(client *mongo.Client, dbName string) *HistoryHandler {
	object := HistoryHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("History"),
	}
	return &object
}
