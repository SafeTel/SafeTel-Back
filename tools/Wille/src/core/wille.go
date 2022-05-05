//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	profile "PostmanDbDataImplementation/core/Account"
	blacklist "PostmanDbDataImplementation/core/AccountLists/Blacklist"
	history "PostmanDbDataImplementation/core/AccountLists/History"
	whitelist "PostmanDbDataImplementation/core/AccountLists/Whitelist"
	box "PostmanDbDataImplementation/core/Embedded"
	utils "PostmanDbDataImplementation/core/Utils"
	print "PostmanDbDataImplementation/core/Utils/Print"
	"bufio"
	"context"
	"errors"
	"fmt"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"

	"time"
)

type Wille struct {
	Client                 *mongo.Client
	DBForUsers             *mongo.Database
	DBForBox               *mongo.Database
	DBForApiKey            *mongo.Database
	Blacklist              *blacklist.Blacklist
	Whitelist              *whitelist.Whitelist
	History                *history.History
	Profile                *profile.Profile
	Box                    *box.Box
	Print                  *print.Print
	ApiKey                 string
	DEV_DB_CLIENT          string
	DEV_DB_PASSWORD        string
	DEV_DB_USERS_NAME      string
	DEV_DB_BOXES_NAME      string
	DEV_DB_DEVELOPERS_NAME string
	DEV_URI_USERS_DB       string
	DEV_URI_BOXES_DB       string
}

// Print help
func (wille *Wille) printHelp() {
	file, err := os.Open("src/help.txt")

	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

// Random command
// generate randomly a new user to upload on the db
func (wille *Wille) random(name string) error {
	wille.Print.Info(name)
	return nil
}

// Compute Input command
// options: command + parameter in input
func (wille *Wille) compute(options []string) error {
	var optionsNumber int = len(options)

	for i := 0; i < optionsNumber; i++ {
		switch options[i] {
		case "--apikey":
			if (i + 1) >= optionsNumber {
				return errors.New("Missing user argument for apikey command")
			}
			i++
			err := wille.apikey(options[i])
			return err
		case "--random":
			if (i + 1) >= optionsNumber {
				return errors.New("Missing user argument for random command")
			}
			i++
			err := wille.random(options[i])
			return err
		case "--show":
			if (i + 1) >= optionsNumber {
				return errors.New("Missing model name for show command")
			}
			i++
			err := wille.show(options[i])
			return err
		case "--upload":
			if (i + 1) >= optionsNumber {
				return errors.New("Missing model name for upload command")
			}
			i++
			err := wille.upload(options[i])
			return err
		case "--hash":
			if (i + 1) >= optionsNumber {
				return errors.New("Missing password for hash command")
			}
			i++
			err := wille.hash(options[i])
			return err
		case "--help":
			wille.printHelp()
			return nil
		default:
			wille.printHelp()
			return errors.New("Unknow Input: " + options[i])
		}
	}
	return nil
}

func (wille *Wille) Run(withOptions []string) error {
	if err := wille.compute(withOptions); err != nil {
		return err
	}
	return nil
}

func New() (*Wille, error) {
	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	}
	serverAPIOptions := options.ServerAPI(options.ServerAPIVersion1)
	DEV_URI_USERS_DB := config.DEV_URI_USERS_DB
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

	wille.DEV_DB_CLIENT = config.DEV_DB_CLIENT
	wille.DEV_DB_PASSWORD = config.DEV_DB_PASSWORD
	wille.DEV_DB_USERS_NAME = config.DEV_DB_USERS_NAME
	wille.DEV_DB_BOXES_NAME = config.DEV_DB_BOXES_NAME
	wille.DEV_DB_DEVELOPERS_NAME = config.DEV_DB_DEVELOPERS_NAME
	wille.DEV_URI_USERS_DB = config.DEV_URI_USERS_DB
	wille.DEV_URI_BOXES_DB = config.DEV_URI_BOXES_DB

	wille.DBForUsers = wille.Client.Database(wille.DEV_DB_USERS_NAME)
	wille.DBForBox = wille.Client.Database(wille.DEV_DB_BOXES_NAME)
	wille.DBForApiKey = wille.Client.Database(wille.DEV_DB_DEVELOPERS_NAME)
	wille.Print = print.New()
	wille.Blacklist, err = blacklist.New(wille.Client, wille.Print)

	wille.ApiKey = ""

	if err != nil {
		return nil, err
	}
	wille.Whitelist, err = whitelist.New(wille.Client, wille.Print)

	if err != nil {
		return nil, err
	}
	wille.History, err = history.New(wille.Client, wille.Print)

	if err != nil {
		return nil, err
	}
	wille.Profile, err = profile.New(wille.Client, wille.Print)

	if err != nil {
		return nil, err
	}
	wille.Box, err = box.New(wille.Client, wille.Print)

	if err != nil {
		return nil, err
	}
	return &wille, nil
}
