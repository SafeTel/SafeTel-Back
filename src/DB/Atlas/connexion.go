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
	"time"

	"go.mongodb.org/mongo-driver/mongo" // Mongo Driver
	"go.mongodb.org/mongo-driver/mongo/options"
)

const ( // Global vars
	DBName     = "Melchior"                                                                                                                              // Data base name
	DBPassword = "aSEFTHUKOM1!"                                                                                                                          // Data base user password
	URI        = "mongodb+srv://SafeTelBackEndUser:" + DBPassword + "@safetel-back-cluster.klq5k.mongodb.net/" + DBName + "?retryWrites=true&w=majority" // Uri of the mongoAtlas data base
	// TODO: explicit
	// FIXME: comment
)

func generateAMongoClient() *mongo.Client { // Generate a mongoDb atlas client
	log.Println("Try to connect client to MongoDB Atlas!")
	client, err := mongo.NewClient(options.Client().ApplyURI(URI)) // Generating a new client

	if err != nil {
		log.Fatal(err)
	}
	return client
}

func checkIfClientIsConnected(client *mongo.Client, ctx context.Context) { // Check if the client is connected to his mongo db
	// Check the connection
	if err := client.Ping(ctx, nil); err != nil {
		log.Fatal(err)
	}
	log.Println("Client Connected to MongoDB!")
}

func connectClientToMongoDb(client *mongo.Client, ctx context.Context) { // Connect a client to mongoDbAtlas
	connectionCtx, cleanContextDatas := context.WithTimeout(ctx, 10*time.Second) // generating a basic context (context.Background) + with timeout

	defer cleanContextDatas()            // Cancel mean cleaning datas in the context (free data)
	err := client.Connect(connectionCtx) // Connecting the client to the database
	if err != nil {                      // Check Error
		log.Fatal(err)
	}
}

func GetConnectedMongoAtlasClient() *mongo.Client { // Create and return a client connected to the project mongoDB Atlas
	client := generateAMongoClient() // Generate a mongo Client
	ctx := context.Background()      // Generate a basic ctx

	connectClientToMongoDb(client, ctx)   // Connect the mongo Client
	checkIfClientIsConnected(client, ctx) // Check client connexion
	return client
}
