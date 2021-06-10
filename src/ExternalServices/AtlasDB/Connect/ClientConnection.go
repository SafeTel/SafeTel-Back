//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - ClientConnection.go
//

package mongoDBAtlasClient

import (
	"context"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/mongo"         // Mongo Driver
	"go.mongodb.org/mongo-driver/mongo/options" // Mongo Driver Options
)

var LogFatal = log.Fatal // Encapsulation of func that can be modify for test

func generateAMongoClient() *mongo.Client {
	log.Println("Try to connect client to MongoDB Atlas!")
	mongoAtlasClusterURI := os.Getenv("MongoAtlasClusterURI")

	if mongoAtlasClusterURI == "" {
		if _, exist := os.LookupEnv("MongoAtlasClusterURI"); !exist {
			LogFatal("MongoAtlasClusterURI env var have not been set")
		}
		LogFatal("mongoAtlasClusterURI env var empty")
	}

	client, err := mongo.NewClient(options.Client().ApplyURI(mongoAtlasClusterURI)) // Generating a new client

	if err != nil {
		LogFatal(err)
	}
	return client
}

func connectClientToAtlasMongoDb(client *mongo.Client, ctx context.Context) {
	connectionCtx, cleanContextDatas := context.WithTimeout(ctx, 10*time.Second) // generating a basic context (context.Background) + with timeout

	defer cleanContextDatas() // Cancel mean cleaning datas in the context (free data)
	err := client.Connect(connectionCtx)
	if err != nil {
		LogFatal(err)
	}
}

func CreateConnectionToAtlas() *mongo.Client { // Create and return a client connected to the project mongoDB Atlas
	client := generateAMongoClient()
	ctx := context.Background()

	connectClientToAtlasMongoDb(client, ctx)
	if err := client.Ping(ctx, nil); err != nil {
		LogFatal(err)
	}
	return client
}
