//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/cmd/WILLE/errors"
	"context"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
	"log"
	"time"
)

type Wille struct {
	Client    *mongo.Client
	DB        *mongo.Database
	Blacklist *mongo.Collection
	History   *mongo.Collection
	Whitelist *mongo.Collection
	User      *mongo.Collection
	Greylist  *mongo.Collection
}

func (wille *Wille) post(collection *mongo.Collection, jsonForRequest string) (interface{}, error) {
	_, err := collection.InsertOne(nil, []interface{}{bson.D{{"", ""}, {"", ""}, {"", ""}}})

	if err != nil {
		log.Println()
	}

	return nil, nil
}

func (wille *Wille) computeRandom(userName string) error {
	log.Println(userName)
	return nil
}

func (wille *Wille) computeCustom(path string) error {
	log.Println(path)
	return nil
}

func (wille *Wille) parseAndCompute(path string) error {
	log.Println(path)
	return nil
}

func (wille *Wille) treat(options []string) error {

	for i := 0; i < len(options); i++ {
		switch options[i] {
		case "random":
			if (i + 1) >= len(options) {
				return &input.Error{Msg: "Missing user argument for random option flag"}
			}
			i++
			wille.computeRandom(options[i])
			return nil
		case "custom":
			if (i + 1) >= len(options) {
				return &input.Error{Msg: "Missing file path for custom option flag"}
			}
			i++
			wille.computeCustom(options[i])
			return nil
		default:
			wille.parseAndCompute(options[i])
		}

	}
	return nil
}

func (wille *Wille) Run(withOptions []string) error {

	log.Println("Running Wille")

	err := wille.treat(withOptions)

	if err != nil {
		log.Println(err)
	}
	return nil
}

func New() (*Wille, error) {
	serverAPIOptions := options.ServerAPI(options.ServerAPIVersion1)
	clientOptions := options.Client().
		ApplyURI(DEV_URI_USERS_DB).
		SetServerAPIOptions(serverAPIOptions)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, clientOptions)

	if err != nil {
		log.Fatal(err)
	}

	wille := Wille{Client: client}
	wille.DB = wille.Client.Database("Melchior")
	wille.Blacklist = wille.DB.Collection("Blacklist")
	wille.History = wille.DB.Collection("History")
	wille.Whitelist = wille.DB.Collection("Whitelist")
	wille.User = wille.DB.Collection("User")
	wille.Greylist = wille.DB.Collection("Greylist")

	return &wille, nil
}
