//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - NewHistory.go
//

package historyCollections

import (
	"go.mongodb.org/mongo-driver/mongo"
)

type HistoryHandler struct {
	client     *mongo.Client
	dataBase   *mongo.Database
	collection *mongo.Collection
}

func NewHistory(client *mongo.Client, dbName string) *HistoryHandler {
	object := HistoryHandler{
		client:     client,
		dataBase:   client.Database(dbName),
		collection: client.Database(dbName).Collection("History"),
	}
	return &object
}
