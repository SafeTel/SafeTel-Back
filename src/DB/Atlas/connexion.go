package mongoDBAtlas

import (
	"context"
	"errors"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"         // Mongo Driver
	"go.mongodb.org/mongo-driver/mongo/options" // Mongo Driver
	// Mongo Driver
)

// Global vars
const (
	DBName = "Melchior" // Data base name

	DBPassword = "aSEFTHUKOM1!" // Data base user password

	URI = "mongodb+srv://admin:" + DBPassword + "@cluster0.7yreq.mongodb.net/" + DBName + "?retryWrites=true&w=majority" // Uri of the mongoAtlas data base
)

func generateAMongoClient() (*mongo.Client, error) {
	log.Println("Try to connect client to MongoDB Atlas!")         // Printing to ensure the program started
	client, err := mongo.NewClient(options.Client().ApplyURI(URI)) // Generating a new client

	if err != nil {
		return nil, err
	}
	return client, nil
}

func checkIfClienIsConnected(client *mongo.Client, ctx context.Context) error {
	err := client.Ping(ctx, nil) // Check the connection

	if err != nil { // Check Error
		return err
	}
	log.Println("Client Connected to MongoDB!") // Checked connection
	return nil
}

func connectClientToMongoDb(client *mongo.Client, ctx context.Context) error {
	connectionCtx, cancel := context.WithTimeout(ctx, 10*time.Second) // generating a basic context (context.Background) + with timeout <=> return a WithDeadline(parent, time.Now().Add(timeOut)) ::  WithDeadline returns a copy of the parent context with the deadline adjusted to be no later than d. If the parent's deadline is already earlier than d, WithDeadline(parent, d) is semantically equivalent to parent. The returned context's Done channel is closed when the deadline expires, when the returned cancel function is called, or when the parent context's Done channel is closed, whichever happens first.

	defer cancel()                       // Cancel mean cleaning datas in the context (free data)
	err := client.Connect(connectionCtx) // Connecting the client to the database

	if err != nil { // Check Error
		return err
	}
	return nil
}

func GetConnectedMongoAtlasClient(isExitingIfErrors bool) (*mongo.Client, error) {
	client, err := generateAMongoClient() // Generate a mongo Client
	ctx := context.Background()           // Generate a basic ctx

	if err != nil { // Check generation of Mongo Client
		if isExitingIfErrors { // Exiting the program if their is an error
			log.Fatal(err) // log and Exit(1)
		}
		return nil, errors.New("Error: Generation of Mongo Client: " + err.Error())
	}

	err = connectClientToMongoDb(client, ctx) // Connect the mongo Client

	if err != nil { // Check connection to mongo db
		if isExitingIfErrors { // Exiting the program if their is an error
			log.Fatal(err) // log and Exit(1)
		}
		return nil, errors.New("Error: Connection to Mongo Client: " + err.Error())
	}

	return client, nil
}

// --- Client Deconnection --- //

func DisconnectMongoAtlasClient(client *mongo.Client, isExitingIfErrors bool) error { // Disconnect function disconnecting the client to the server
	err := client.Disconnect(context.Background()) // Disconnection the client in the default context context.Background()

	if err != nil { // Check Errors
		if isExitingIfErrors { // Exiting the program if their is an error
			log.Fatal(err) // log and Exit(1)
		}
		return errors.New("Error: Disconnection of Mongo Client: " + err.Error())
	}

	log.Println("Connection to MongoDB closed.")
	return nil
}
