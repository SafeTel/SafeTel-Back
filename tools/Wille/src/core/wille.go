//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"bytes"
	"context"
	"errors"
	"os"
	"os/exec"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
	"log"
	"time"
)

// Structure used to check environnement variable validity
type Config struct {
	MandatoryEnvVars []string `json:"MandatoryEnvVars"`
}

type Wille struct {
	Client                 *mongo.Client
	DB                     *mongo.Database
	Blacklist              *mongo.Collection
	History                *mongo.Collection
	Whitelist              *mongo.Collection
	User                   *mongo.Collection
	Greylist               *mongo.Collection
	DEV_DB_CLIENT          string
	DEV_DB_PASSWORD        string
	DEV_DB_USERS_NAME      string
	DEV_DB_DEVELOPERS_NAME string
	DEV_URI_USERS_DB       string
}

// Global Var

var (
	WarningLogger *log.Logger
	InfoLogger    *log.Logger
	ErrorLogger   *log.Logger
)

var ResetColor = "\033[0m"
var Red = "\033[31m"
var Green = "\033[32m"
var Yellow = "\033[33m"
var Blue = "\033[34m"
var Cyan = "\033[36m"
var valid byte = 1
var tabPrefixForJsonPrint = "\t\t"

// Mongo Import
// Execute a bash command
// mongoimport: allow to upload a file on a mongo db inside a specific collection
func (wille *Wille) mongoImport(uri, collection, file string) (err error, onStdOut string, onStdErr string) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	// Specifing command: 	mongoimport (import content; JSON, CSV, TSV)
	//						uri (perform command on this mongo database)
	//						collection (perform command on this collection of the mongo database)
	//						file (the file that has to be imported)
	bashCommand := exec.Command("mongoimport", "--uri", uri, "--collection", collection, "--file", file)
	bashCommand.Stdout = &stdout // assing command I/O stdout to get exec package stdout
	bashCommand.Stderr = &stderr // assign command I/O stderr to get exec package stderr
	// Start the specified command and waits for it to complete
	err = bashCommand.Run()
	return err, stdout.String(), stderr.String()
}

func (wille *Wille) Run(withOptions []string) error {
	if err := wille.compute(withOptions); err != nil {
		return err
	}
	return nil
}

func checkEnv() error {
	var config Config

	// Get Mandatory env variable
	decoder, err := OpenAndGenerateJsonDecoder("src/config.json")
	if err != nil {
		return err
	}
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&config); err != nil {
		return err
	}

	for _, envVar := range config.MandatoryEnvVars {
		if value, isSet := os.LookupEnv(envVar); !isSet || value == "" {
			return errors.New("Problem with Environment variables: " + envVar + " is not set")
		}
	}
	return nil
}

func NewWille() (*Wille, error) {
	if err := checkEnv(); err != nil {
		return nil, err
	}
	serverAPIOptions := options.ServerAPI(options.ServerAPIVersion1)
	DEV_URI_USERS_DB := os.Getenv("DEV_URI_USERS_DB")
	clientOptions := options.Client().
		ApplyURI(DEV_URI_USERS_DB).
		SetServerAPIOptions(serverAPIOptions)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	defer cancel()
	client, err := mongo.Connect(ctx, clientOptions)

	if err != nil {
		return nil, err
	}
	wille := Wille{Client: client}
	wille.DB = wille.Client.Database("Melchior")
	wille.Blacklist = wille.DB.Collection("Blacklist")
	wille.History = wille.DB.Collection("History")
	wille.Whitelist = wille.DB.Collection("Whitelist")
	wille.User = wille.DB.Collection("User")
	wille.Greylist = wille.DB.Collection("Greylist")

	wille.DEV_DB_CLIENT = os.Getenv("DEV_DB_CLIENT")
	wille.DEV_DB_PASSWORD = os.Getenv("DEV_DB_PASSWORD")
	wille.DEV_DB_USERS_NAME = os.Getenv("DEV_DB_USERS_NAME")
	wille.DEV_DB_DEVELOPERS_NAME = os.Getenv("DEV_DB_DEVELOPERS_NAME")
	wille.DEV_URI_USERS_DB = DEV_URI_USERS_DB

	InfoLogger = log.New(os.Stdin, "", log.Ldate|log.Ltime)
	WarningLogger = log.New(os.Stderr, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLogger = log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lmicroseconds|log.Lshortfile)
	return &wille, nil
}
