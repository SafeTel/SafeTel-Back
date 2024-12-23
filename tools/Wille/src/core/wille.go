//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	profile "PostmanDbDataImplementation/core/Account"                  // Profile data structure
	blacklist "PostmanDbDataImplementation/core/AccountLists/Blacklist" // Blacklist data structure
	history "PostmanDbDataImplementation/core/AccountLists/History"     // History data structure
	whitelist "PostmanDbDataImplementation/core/AccountLists/Whitelist" // Whitelist data structure
	box "PostmanDbDataImplementation/core/Embedded"                     // Embedded data structure
	utils "PostmanDbDataImplementation/core/Utils"                      // Utils for config.json file
	print "PostmanDbDataImplementation/core/Utils/Print"                // Print data structure
	"bufio"                                                             // Read a File line per line
	"context"                                                           // Configure Mongo client
	"errors"

	// Generate new errors
	"fmt" // Printing using println
	"log" // Logging
	"os"  // Open a File

	"go.mongodb.org/mongo-driver/mongo"         // Generate Clients
	"go.mongodb.org/mongo-driver/mongo/options" // Configure Clients with Options

	"time" // Timeout
)

type Wille struct {
	Client      *mongo.Client
	DBForUsers  *mongo.Database
	DBForBox    *mongo.Database
	DBForApiKey *mongo.Database
	Blacklist   *blacklist.Blacklist
	Whitelist   *whitelist.Whitelist
	History     *history.History
	Profile     *profile.Profile
	Box         *box.Box
	Print       *print.Print
	ApiKey      string
}

type CommandFunctionType func(string) error

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
func (wille *Wille) compute(options []string, functions map[string]CommandFunctionType) error {
	var optionsNumber int = len(options)

	for i := 0; i < optionsNumber; i++ {
		switch options[i] {
		case "--help":
			wille.printHelp()
			return nil
		default:
			function := functions[options[i]]

			if function == nil {
				return errors.New("Unknow Input: " + options[i])
			}
			if (i + 1) >= optionsNumber {
				return errors.New("Missing argument for " + options[i] + " command")
			}
			i++
			if err := function(options[i]); err != nil {
				return err
			}
		}
	}
	return nil
}

func (wille *Wille) Run(withOptions []string) error {
	functions := map[string]CommandFunctionType{
		"--apikey": wille.apikey,
		"--random": wille.random,
		"--show":   wille.show,
		"--upload": wille.upload,
		"--hash":   wille.hash}

	if err := wille.compute(withOptions, functions); err != nil {
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

	wille.DBForUsers = wille.Client.Database(config.DEV_DB_USERS_NAME)
	wille.DBForBox = wille.Client.Database(config.DEV_DB_BOXES_NAME)
	wille.DBForApiKey = wille.Client.Database(config.DEV_DB_DEVELOPERS_NAME)
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
