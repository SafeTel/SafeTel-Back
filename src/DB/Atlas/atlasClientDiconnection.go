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

	"go.mongodb.org/mongo-driver/mongo" // Mongo Driver
)

func DisconnectMongoAtlasClient(client *mongo.Client) { // Disconnect function disconnecting the client to the server
	err := client.Disconnect(context.Background()) // Disconnection the client in the default context context.Background()

	if err != nil { // Check Errors
		log.Panic(err)
	}
	log.Println("Connection to MongoDB closed.")
}
