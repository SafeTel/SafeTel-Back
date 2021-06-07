//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - NewWhiteList.go
//

package whitelistCollections

import (
	"go.mongodb.org/mongo-driver/mongo"
)

type WhitelistHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func NewWhilelist(client *mongo.Client, dbName string) *WhitelistHandler {
	object := WhitelistHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("Whitelist"),
	}
	return &object
}
