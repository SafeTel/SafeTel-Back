//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	// Uploader data structure
	uploader "PostmanDbDataImplementation/core/Uploader"
	// Utils for config.json file
	utils "PostmanDbDataImplementation/core/Utils"
	// Print data structure
	print "PostmanDbDataImplementation/core/Utils/Print"
	// Mongo Utils
	mongoUtils "PostmanDbDataImplementation/core/Utils/Mongo"

	// Read a File line per line
	"bufio"
	// Configure Mongo client

	// Generate new errors
	"errors"
	// Printing using println
	"fmt"
	// Logging
	"log"
	// Open a File
	"os"
	// Mongo.Client type
	"go.mongodb.org/mongo-driver/mongo"
)

type Wille struct {
	Client      *mongo.Client
	DBForApiKey *mongo.Database
	Config      *utils.Config

	Uploader *uploader.Uploader
	Print    *print.Print
	ApiKey   string
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
		"--apikey":      wille.apikey,
		"--random":      wille.random,
		"--show":        wille.show,
		"--upload":      wille.upload,
		"--uploadBoxes": wille.uploadBoxes,
		"--hash":        wille.hash}

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

	client, err := mongoUtils.GenerateClient(config.DEV_URI_USERS_DB)

	if err != nil {
		return nil, err
	}
	wille := Wille{Client: client}
	wille.ApiKey = ""
	wille.DBForApiKey = wille.Client.Database(config.DEV_DB_DEVELOPERS_NAME)
	wille.Config = config
	wille.Print = print.New()

	wille.Uploader, err = uploader.New(wille.Client, wille.Print, wille.Config)

	if err != nil {
		return nil, err
	}

	return &wille, nil
}
