//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"context"
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"
	"reflect"
	"strconv"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
)

type JsonWorker struct {
	ctx context.Context
}

func (jsonWorker *JsonWorker) printEmptyOrUndefinedKey(key string) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[31mEmpty or not defined\033[0m")
}

func (jsonWorker *JsonWorker) printDefinedKeyWithValue(key string, value interface{}) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[32mdefined\033[0m Value: \033[36m", value, ResetColor)
}

func (jsonWorker *JsonWorker) openAndUnmarshalJson(path string) (map[string]interface{}, error) {
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

// Check if the Collection given as first argument contain the elements finded using the filter
// If it's the case, return an error stipulating the data has already been posted on the db
// Otherwise, return nil
func (jsonWorker *JsonWorker) checkDataValidity(col *mongo.Collection, filter bson.M) error {
	var isDocument []bson.M
	cursor, err := col.Find(context.TODO(), filter)

	if err != nil {
		return err
	}
	// Check if some documents have been founded
	err = cursor.All(context.TODO(), &isDocument)

	if isDocument != nil {
		return errors.New("Data already exist inside the server")
	}
	return nil
}

// Parse the content of the Map of a json map value
// This map is called by checkJsonContent, and call this function RECURSIVELY
func (jsonWorker *JsonWorker) checkJsonMap(mapContent map[string]interface{}, key string, jsonObjectKeysInOrder []string) ([]string, error) {
	lenMapContent := len(mapContent)
	lenIdObjects := len(jsonObjectKeysInOrder)
	if lenIdObjects < lenMapContent {
		return nil, errors.New("Missing identifier of Object for json var: \033[31m" + key + ResetColor + ". Len value: " + strconv.Itoa(lenIdObjects))
	}
	err := jsonWorker.checkJsonContent(mapContent, jsonObjectKeysInOrder[0:lenMapContent], jsonObjectKeysInOrder[lenMapContent:])

	if err != nil {
		return nil, err
	}

	return jsonObjectKeysInOrder[lenMapContent:], nil
}

// Parse the content of the json and interpret the keys:
// jsonKeysInOrder: the order of the elements inside the json, in the same order than inside the json (same order for parsing optimisation reasons)
//					In this way, the jsonContent is parse, and when a key is not founded, is missing, or if the value is empty, it print it and return an error
// jsonObjectKeysInOrder:	The order of the elements of an object inside the json, in order for the same reasons as jsonKeysInOrder
//							This allow better printing, error handling, and better logic
// The idea behind this function is to parse and check the json in this way:
// json example: {					jsonKeysInOrder:	[		jsonObjectKeysInOrder:
//		"A": "a", -> 									"A",
// 		"B": "b",										"B",
//		"C": {											"C"							.:	[
//				"a_of_C": a_Of_C						]								"a_of_C"
//		}																				]
// }
func (jsonWorker *JsonWorker) checkJsonContent(jsonContent map[string]interface{}, jsonKeysInOrder []string, jsonObjectKeysInOrder []string) error {
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
				jsonObjectKeysInOrder, err = jsonWorker.checkJsonMap(jsonContent[key].(map[string]interface{}), key, jsonObjectKeysInOrder)
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

// Same as checkJsonMap function:
// 		Called by checkAndShowJsonContent and call it for printing
func (jsonWorker *JsonWorker) checkAndShowJsonMap(mapContent map[string]interface{}, key string, jsonObjectKeysInOrder []string) ([]string, error) {
	lenMapContent := len(mapContent)
	lenIdObjects := len(jsonObjectKeysInOrder)
	// Check if the json object array has enought keys to check the content of the json map content
	if lenIdObjects < lenMapContent {
		return nil, errors.New("Missing identifier of Object for json var: \033[31m" + key + ResetColor + ". Len value: " + strconv.Itoa(lenIdObjects))
	}
	// add a tab to prefix
	tabPrefixForJsonPrint += "\t"
	err := jsonWorker.checkAndShowJsonContent(mapContent, jsonObjectKeysInOrder[0:lenMapContent], jsonObjectKeysInOrder[lenMapContent:])

	if err != nil {
		return nil, err
	}
	// reset the prefix to basic value
	tabPrefixForJsonPrint = "\t\t"

	// return the jsonObjectKeysInOrder without the keys of the json map
	return jsonObjectKeysInOrder[lenMapContent:], nil
}

// Same as checkJsonContent function:
// 		Print the finded results
func (jsonWorker *JsonWorker) checkAndShowJsonContent(jsonContent map[string]interface{}, jsonKeysInOrder []string, jsonObjectKeysInOrder []string) error {
	lenIdentifiers := len(jsonKeysInOrder)
	key := ""
	// Check if the json content has the same number of elements than the values to checks
	if len(jsonContent) != lenIdentifiers {
		return errors.New("Content and Identifier have to be the same size for checking json content. Number of identifiers expeted: " + strconv.Itoa(lenIdentifiers) + ", Founded: " + strconv.Itoa(len(jsonContent)))
	}
	for i := 0; i < lenIdentifiers; i++ {
		// Get key value
		key = jsonKeysInOrder[i]
		// Check the type of the key value
		switch reflect.ValueOf(jsonContent[key]).Kind() {
		case reflect.Map:
			if jsonContent[key] == nil {
				jsonWorker.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				jsonWorker.printDefinedKeyWithValue(key, jsonContent[key])
				var err error
				// Check the content of the json object and print the content.
				// The content of the json object is the content stored inside the 3th parameter of the function
				jsonObjectKeysInOrder, err = jsonWorker.checkAndShowJsonMap(jsonContent[key].(map[string]interface{}), key, jsonObjectKeysInOrder)
				if err != nil {
					return err
				}
			}
		case reflect.String:
			if jsonContent[key] == "" {
				jsonWorker.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				jsonWorker.printDefinedKeyWithValue(key, jsonContent[key])
			}
		// Type of an array when stored inside a variable of type: map[string]interface{}
		case reflect.TypeOf([]interface{}{}).Kind():
			if jsonContent[key] == nil {
				jsonWorker.printEmptyOrUndefinedKey(key)
				return errors.New("Missing value inside json")
			} else {
				jsonWorker.printDefinedKeyWithValue(key, jsonContent[key])
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

// Check the content of the Lists folder and print it
func (jsonWorker *JsonWorker) checkShowJsonContent(name string) error {
	s, err := jsonWorker.openAndUnmarshalJson("data/" + name + "/Show.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"infos",
		"password"}

	err = jsonWorker.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Show.json" + ": " + err.Error())
	}
	return nil
}

func NewJsonWorker() (*JsonWorker, error) {
	jsonWorker := JsonWorker{ctx: context.TODO()}

	// wille.DB = wille.Client.Database("Melchior")
	// wille.Blacklist = wille.DB.Collection("Blacklist")
	// wille.History = wille.DB.Collection("History")
	// wille.Whitelist = wille.DB.Collection("Whitelist")
	// wille.User = wille.DB.Collection("User")
	// wille.Greylist = wille.DB.Collection("Greylist")
	// wille.JsonWorker = cmd.NewJsonWorker()

	// InfoLogger = log.New(os.Stdin, "", log.Ldate|log.Ltime)
	// WarningLogger = log.New(os.Stderr, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	// ErrorLogger = log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lmicroseconds|log.Lshortfile)

	return &jsonWorker, nil
}
