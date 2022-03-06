//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/cmd/WILLE/errors"
	"bytes"
	"context"
	"errors"
	"io/ioutil"
	"os"
	"os/exec"
	"reflect"
	"strconv"

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

// Domain Layer - Core Functionalities

func (wille *Wille) mongoImport(uri, collection, file string) (err error, onStdOut string, onStdErr string) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	cmd := exec.Command("mongoimport", "--uri", uri, "--collection", collection, "--file", file)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err = cmd.Run()

	return err, stdout.String(), stderr.String()
}

func (wille *Wille) printEmptyOrUndefinedKey(key string) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[31mEmpty or not defined\033[0m")
}

func (wille *Wille) printDefinedKeyWithValue(key string, value interface{}) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[32mdefined\033[0m Value: \033[36m", value, ResetColor)
}

func (wille *Wille) checkJsonContent(jsonContent map[string]interface{}, identifiersInSameOrderThanJson []string, identifierOfObjectSameOrderThanJson []string) error {
	lenIdentifiers := len(identifiersInSameOrderThanJson)
	key := ""

	if len(jsonContent) != lenIdentifiers {
		return errors.New("Content and Identifier have to be the same size for checking json content")
	}
	for i := 0; i < lenIdentifiers; i++ {
		key = identifiersInSameOrderThanJson[i]

		switch reflect.ValueOf(jsonContent[key]).Kind() {
		case reflect.Map:
			if jsonContent[key] == nil {
				wille.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				wille.printDefinedKeyWithValue(key, jsonContent[key])
				mapContent := jsonContent[key].(map[string]interface{})
				lenMapContent := len(mapContent)
				lenIdObjects := len(identifierOfObjectSameOrderThanJson)
				if lenIdObjects < lenMapContent {
					return errors.New("Missing identifier of Object for json var: \033[31m" + key + ResetColor + ". Len value: " + strconv.Itoa(lenIdObjects))
				}
				tabPrefixForJsonPrint += "\t"
				wille.checkJsonContent(mapContent, identifierOfObjectSameOrderThanJson[0:lenMapContent], identifierOfObjectSameOrderThanJson[lenMapContent:])
				identifierOfObjectSameOrderThanJson = identifierOfObjectSameOrderThanJson[lenMapContent:]
				tabPrefixForJsonPrint = "\t\t"
			}
		case reflect.String:
			if jsonContent[key] == "" {
				wille.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				wille.printDefinedKeyWithValue(key, jsonContent[key])
			}
		case reflect.TypeOf([]interface{}{}).Kind():
			if jsonContent[key] == nil {
				wille.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				wille.printDefinedKeyWithValue(key, jsonContent[key])
			}
		default:
			InfoLogger.Println(tabPrefixForJsonPrint, "-\033[33m", key, "\033[0mType content: \033[33m", reflect.TypeOf(jsonContent[key]), "\033[0m |!!!|\033[31mNOT HANDLED\033[0m|!!!|")
		}
	}
	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkListJsonFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("Data/" + name + "/List")
	if err != nil {
		return 0, &input.Error{Msg: "Unable to open list folder for name: " + name + ". Not Found: Data/" + name + "/List"}
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

func (wille *Wille) checkModelFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("Data/" + name)

	if err != nil {
		return 0, &input.Error{Msg: "Unable to open folder for name: " + name + ". Not Found: Data/" + name}
	}

	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Profile.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "List" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Show.json" {
			content ^= byte(0b00000100)
		} else {
			InfoLogger.Println("Unknow Content: \033[33m", anElem.Name(), "\033[0m")
		}
	}
	return content, nil
}

// Repository Layer

func (wille *Wille) uploadListFile(name string) error {
	content, err := wille.checkListJsonFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadBlacklistFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadHistoryFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000100)>>2 == valid {
		err = wille.uploadWhitelistFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}

// Service Layer - Interface

func (wille *Wille) showListFolder(name string) error {
	listFolderContent, err := wille.checkListJsonFolder(name)

	if err != nil {
		return err
	}
	if listFolderContent&(0b00000001) == valid {
		InfoLogger.Println("\t- Blacklist.json: \033[32mFinded\033[0m")
		err = wille.checkBlacklistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Blacklist.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("\t- History.json: \033[32mFinded\033[0m")
		err = wille.checkHistoryJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- History.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("\t- Whitelist.json: \033[32mFinded\033[0m")
		err = wille.checkWhitelistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Whitelist.json: \033[32mMissing\033[0m")
	}
	return nil
}

func (wille *Wille) show(name string) error {
	modelFolderContent, err := wille.checkModelFolder(name)

	if err != nil {
		return err
	}
	if modelFolderContent&(0b00000001) == valid {
		InfoLogger.Println("Profile.json: \033[32mFinded\033[0m")
		err = wille.checkProfileJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Profile.json: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("List folder: \033[32mFinded\033[0m")
		err = wille.showListFolder(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("List folder: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("Show.json: \033[32mFinded\033[0m")
		err = wille.checkShowJsonContent(name)
		if err != nil {
			return err
		}
		err = wille.printShowJsonFile(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Show.json: \033[31mMissing\033[0m")
	}
	return nil
}

func (wille *Wille) random(name string) error {
	InfoLogger.Println(name)
	return nil
}

func (wille *Wille) custom(path string) error {
	InfoLogger.Println(path)
	return nil
}

func (wille *Wille) upload(name string) error {
	content, err := wille.checkModelFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadProfileFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010) == valid {
		err = wille.uploadListFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}

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
		default:
			return &input.Error{Msg: "Unknow pattern"}
		}
	}
	return nil
}

func (wille *Wille) Run(withOptions []string) error {

	InfoLogger.Println("Running Wille")

	err := wille.compute(withOptions)

	if err != nil {
		return err
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
		return nil, err
	}
	wille := Wille{Client: client}
	wille.DB = wille.Client.Database("Melchior")
	wille.Blacklist = wille.DB.Collection("Blacklist")
	wille.History = wille.DB.Collection("History")
	wille.Whitelist = wille.DB.Collection("Whitelist")
	wille.User = wille.DB.Collection("User")
	wille.Greylist = wille.DB.Collection("Greylist")

	InfoLogger = log.New(os.Stdin, "", log.Ldate|log.Ltime)
	WarningLogger = log.New(os.Stderr, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLogger = log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lmicroseconds|log.Lshortfile)

	return &wille, nil
}
