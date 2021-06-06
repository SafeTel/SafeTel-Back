//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - connexion.go
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

func generateAMongoClient() *mongo.Client { // Generate a mongoDb atlas client
	log.Println("Try to connect client to MongoDB Atlas!")
	mongoAtlasClusterURI := os.Getenv("MongoAtlasClusterURI")

	if mongoAtlasClusterURI == "" {
		// TODO:haveBeenSet -> exist
		if _, haveBeenSet := os.LookupEnv("MongoAtlasClusterURI"); !haveBeenSet {
			log.Fatal("MongoAtlasClusterURI env var have not been set")
		}
		log.Fatal("mongoAtlasClusterURI env var empty")
	}

	client, err := mongo.NewClient(options.Client().ApplyURI(mongoAtlasClusterURI)) // Generating a new client

	if err != nil {
		log.Fatal(err)
	}
	return client
}

func connectClientToAtlasMongoDb(client *mongo.Client, ctx context.Context) { // Connect a client to mongoDbAtlas
	connectionCtx, cleanContextDatas := context.WithTimeout(ctx, 10*time.Second) // generating a basic context (context.Background) + with timeout

	defer cleanContextDatas()            // Cancel mean cleaning datas in the context (free data)
	err := client.Connect(connectionCtx) // Connecting the client to the database
	if err != nil {
		log.Fatal(err)
	}
}

func CreateConnectionToAtlas() *mongo.Client { // Create and return a client connected to the project mongoDB Atlas
	client := generateAMongoClient()
	ctx := context.Background()

	connectClientToAtlasMongoDb(client, ctx)
	if err := client.Ping(ctx, nil); err != nil {
		log.Fatal(err)
	}
	return client
}
