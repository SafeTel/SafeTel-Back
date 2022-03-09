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
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"reflect"
	"strconv"

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

func (wille *Wille) openAndUnmarshalJson(path string) (map[string]interface{}, error) {
	jsonFile, err := os.Open(path)

	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return nil, err
	}
	var s map[string]interface{}

	err = json.Unmarshal([]byte(byteValue), &s)
	if err != nil {
		return nil, err
	}
	return s, err
}

func (wille *Wille) mongoImport(uri, collection, file string) (err error, onStdOut string, onStdErr string) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	cmd := exec.Command("mongoimport", "--uri", uri, "--collection", collection, "--file", file)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err = cmd.Run()
	return err, stdout.String(), stderr.String()
}

func (wille *Wille) checkDataValidity(col *mongo.Collection, filter bson.M) error {
	var isDocument []bson.M
	cursor, err := col.Find(context.TODO(), filter)

	if err != nil {
		return err
	}
	err = cursor.All(context.TODO(), &isDocument)

	if isDocument != nil {
		return errors.New("Data already exist inside the server")
	}
	return nil
}

func (wille *Wille) printHelp() {
	fmt.Println("\nHelp :")
	fmt.Println("./<binary_name> <command> ")
	fmt.Println("<binary_name>: the name of the binary")
	fmt.Println("<command>: show <data> | upload <data> | help")
	fmt.Println("<data>: The name of a user defined inside the model folder. You can find the available models by doing: ls ./data\n")
}

func (wille *Wille) checkJsonMap(mapContent map[string]interface{}, key string, jsonObjectKeysInOrder []string) ([]string, error) {
	lenMapContent := len(mapContent)
	lenIdObjects := len(jsonObjectKeysInOrder)
	if lenIdObjects < lenMapContent {
		return nil, errors.New("Missing identifier of Object for json var: \033[31m" + key + ResetColor + ". Len value: " + strconv.Itoa(lenIdObjects))
	}
	err := wille.checkJsonContent(mapContent, jsonObjectKeysInOrder[0:lenMapContent], jsonObjectKeysInOrder[lenMapContent:])

	if err != nil {
		return nil, err
	}

	return jsonObjectKeysInOrder[lenMapContent:], nil
}

func (wille *Wille) checkJsonContent(jsonContent map[string]interface{}, jsonKeysInOrder []string, jsonObjectKeysInOrder []string) error {
	lenIdentifiers := len(jsonKeysInOrder)
	key := ""

	if len(jsonContent) != lenIdentifiers {
		return errors.New("Content and Identifier have to be the same size for checking json content. Number of identifiers expeted: " + strconv.Itoa(lenIdentifiers) + ", Founded: " + strconv.Itoa(len(jsonContent)))
	}
	for i := 0; i < lenIdentifiers; i++ {
		key = jsonKeysInOrder[i]

		switch reflect.ValueOf(jsonContent[key]).Kind() {
		case reflect.Map:
			if jsonContent[key] == nil {
				return errors.New("Missing value inside json")
			} else {
				var err error
				jsonObjectKeysInOrder, err = wille.checkJsonMap(jsonContent[key].(map[string]interface{}), key, jsonObjectKeysInOrder)
				if err != nil {
					return err
				}
			}
		case reflect.String:
			if jsonContent[key] == "" {
				return errors.New("Missing value inside json")
			}
		case reflect.TypeOf([]interface{}{}).Kind():
			if jsonContent[key] == nil {
				return errors.New("Missing value inside json")
			}
		default:
			if jsonContent[key] == nil {
				return errors.New("Missing value inside json for key: \033[31m" + key + "\033[0m")
			}
		}
	}
	return nil
}

func (wille *Wille) checkAndShowJsonMap(mapContent map[string]interface{}, key string, jsonObjectKeysInOrder []string) ([]string, error) {
	lenMapContent := len(mapContent)
	lenIdObjects := len(jsonObjectKeysInOrder)
	if lenIdObjects < lenMapContent {
		return nil, errors.New("Missing identifier of Object for json var: \033[31m" + key + ResetColor + ". Len value: " + strconv.Itoa(lenIdObjects))
	}
	tabPrefixForJsonPrint += "\t"
	err := wille.checkAndShowJsonContent(mapContent, jsonObjectKeysInOrder[0:lenMapContent], jsonObjectKeysInOrder[lenMapContent:])

	if err != nil {
		return nil, err
	}
	tabPrefixForJsonPrint = "\t\t"

	return jsonObjectKeysInOrder[lenMapContent:], nil
}

func (wille *Wille) checkAndShowJsonContent(jsonContent map[string]interface{}, jsonKeysInOrder []string, jsonObjectKeysInOrder []string) error {
	lenIdentifiers := len(jsonKeysInOrder)
	key := ""

	if len(jsonContent) != lenIdentifiers {
		return errors.New("Content and Identifier have to be the same size for checking json content. Number of identifiers expeted: " + strconv.Itoa(lenIdentifiers) + ", Founded: " + strconv.Itoa(len(jsonContent)))
	}
	for i := 0; i < lenIdentifiers; i++ {
		key = jsonKeysInOrder[i]

		switch reflect.ValueOf(jsonContent[key]).Kind() {
		case reflect.Map:
			if jsonContent[key] == nil {
				wille.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				wille.printDefinedKeyWithValue(key, jsonContent[key])
				var err error
				jsonObjectKeysInOrder, err = wille.checkAndShowJsonMap(jsonContent[key].(map[string]interface{}), key, jsonObjectKeysInOrder)
				if err != nil {
					return err
				}
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
			if jsonContent[key] == nil {
				return errors.New("Missing value inside json for key: \033[31m" + key + "\033[0m")
			} else {
				InfoLogger.Println(tabPrefixForJsonPrint, "-\033[33m", key, "\033[0mType content: \033[33m", reflect.TypeOf(jsonContent[key]), "\033[0m |!!!|\033[31mNOT HANDLED\033[0m|!!!|")
			}
		}
	}
	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkListJsonFolder(name string) (byte, error) {
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

// Service Layer - Interface

func (wille *Wille) random(name string) error {
	InfoLogger.Println(name)
	return nil
}

func (wille *Wille) custom(path string) error {
	InfoLogger.Println(path)
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
		case "encrypt":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing password for encryption"}
			}
			i++
			err := wille.encrypt(options[i])
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
