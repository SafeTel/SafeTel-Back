//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/errors"
	"bytes"
	"context"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
	"log"
	"time"
)

type Wille struct {
	Client     *mongo.Client
	DB         *mongo.Database
	Blacklist  *mongo.Collection
	History    *mongo.Collection
	Whitelist  *mongo.Collection
	User       *mongo.Collection
	Greylist   *mongo.Collection
	JsonReader *JsonReader
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
var Purple = "\033[35m"
var Cyan = "\033[36m"
var Gray = "\033[37m"
var White = "\033[97m"
var valid byte = 1

var tabPrefixForJsonPrint = "\t\t"

// Print help
func (wille *Wille) printHelp() {
	fmt.Println("\nOVERVIEW: Wille command tool to post data on safetel server")
	fmt.Println("\nUSAGE: ./<binary_name> {command} ")
	fmt.Println("<binary_name>: the name of the binary")
	fmt.Println("command: show <data | upload <data> | hash <password> | help")
	fmt.Println("<data>: The name of a user defined inside the model folder. You can find the available models by doing: ls ./data")
	fmt.Println("<password>: Password to hash\n")
}

// Verify the content of a model folder
// It check if the following files are available:
// data/name:	Profile.json
//				Lists/
//				Show.json
// After reading the folder of the model, it stores inside a BIT the finded elements in the format:
// BIT format:	0b00000001 -> Profile.json file
//				0b00000010 -> Lists folder
//				0b00000100 -> Show.json file
// Print a message when finding an unknown content, with the name in yellow
func (wille *Wille) checkModelFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name)

	if err != nil {
		return 0, &input.Error{Msg: "Unable to open folder for name: " + name + ". Not Found: data/" + name}
	}

	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Profile.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "Lists" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Show.json" {
			content ^= byte(0b00000100)
		} else {
			InfoLogger.Println("Unknow Content: \033[33m", anElem.Name(), "\033[0m")
		}
	}
	return content, nil
}

// Verify the content of a Lists folder
// It check if the following files are available:
// data/name/Lists:	Blacklist.json
//					History.json
//					Whitelist.json
// After reading the Lists folder, it stores inside a BIT the finded elements in the format:
// BIT format:	0b00000001 -> Blacklist.json file
//				0b00000010 -> History.json file
//				0b00000100 -> Whitelist.json file
// Print a message when finding an unknown content, with the name in yellow
func (wille *Wille) checkListFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name + "/Lists")
	if err != nil {
		return 0, &input.Error{Msg: "Unable to open list folder for name: " + name + ". Not Found: data/" + name + "/Lists"}
	}
	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Blacklist.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "History.json" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Whitelist.json" {
			content ^= byte(0b00000100)
		} else {
			InfoLogger.Println("Unknow File: \033[33m", anElem.Name(), "\033[0m")
		}
	}
	return content, nil
}

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

// Random command
// generate randomly a new user to upload on the db
func (wille *Wille) random(name string) error {
	InfoLogger.Println(name)
	return nil
}

// Custom command
// Temporary: Will be removed
func (wille *Wille) custom(path string) error {
	InfoLogger.Println(path)
	return nil
}

// Compute Input command
// options: command + parameter in input
func (wille *Wille) compute(options []string) error {
	var optionsNumber int = len(options)

	for i := 0; i < len(options); i++ {
		switch options[i] {
		case "random":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing user argument for random option flag"}
			}
			i++
			err := wille.random(options[i])
			return err
		case "custom":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing file path for custom option flag"}
			}
			i++
			err := wille.custom(options[i])
			return err
		case "show":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing model name for showing"}
			}
			i++
			err := wille.show(options[i])
			return err
		case "upload":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing model name for upload"}
			}
			i++
			err := wille.upload(options[i])
			return err
		case "hash":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing password for hashion"}
			}
			i++
			err := wille.hash(options[i])
			return err
		case "help":
			wille.printHelp()
			return nil
		default:
			wille.printHelp()
			return &input.Error{Msg: "Unknow pattern"}
		}
	}
	return nil
}

func (wille *Wille) Run(withOptions []string) error {
	err := wille.compute(withOptions)

	if err != nil {
		return err
	}
	return nil
}

func NewWille() (*Wille, error) {
	serverAPIOptions := options.ServerAPI(options.ServerAPIVersion1)
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
	wille.JsonReader, err = NewJsonReader()

	if err != nil {
		return nil, err
	}

	InfoLogger = log.New(os.Stdin, "", log.Ldate|log.Ltime)
	WarningLogger = log.New(os.Stderr, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLogger = log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lmicroseconds|log.Lshortfile)

	return &wille, nil
}
