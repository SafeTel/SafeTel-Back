//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - NewBlackList.go
//

package blacklistCollection

import "go.mongodb.org/mongo-driver/mongo"

type BlacklistHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func NewBlacklist(client *mongo.Client, dbName string) *BlacklistHandler { // Create a new ptr for the class BlacklistHandler
	object := BlacklistHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("Blacklist"),
	}
	return &object
}
