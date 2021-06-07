//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - ClientDisconnection.go
//

package mongoDBAtlasClient

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/mongo" // Mongo Driver
)

func DisconnectMongoAtlasClient(client *mongo.Client) { // Disconnect function disconnecting the client to the server
	err := client.Disconnect(context.Background())

	if err != nil {
		log.Fatal(err)
	}
	log.Println("Connection to MongoDB closed.")
}
