//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package utils

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
)

func OpenAndGenerateJsonDecoder(file string) (*json.Decoder, error) {
	jsonFile, err := os.Open(file)

	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return nil, err
	}
	decoder := json.NewDecoder(bytes.NewReader(byteValue))
	return decoder, nil
}

// Check if the Collection given as first argument contain the elements finded using the filter
// If it's the case, return an error stipulating the data has already been posted on the db
// Otherwise, return nil
func CheckDataValidityOnStorage(col *mongo.Collection, filter bson.M) error {
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

// Verify the content of a model folder
// It check if the following files are available:
// data/name:	Profile.json
//				Lists/
//				Show.json
//				Embedded/
// After reading the folder of the model, it stores inside a BIT the finded elements in the format:
// BIT format:	0b00000001 -> Profile.json file
//				0b00000010 -> Lists folder
//				0b00000100 -> Show.json file
//				0b00001000 -> Embedded folder
// Print a message when finding an unknown content, with the name in yellow
func CheckModelFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name)

	if err != nil {
		return 0, errors.New("Unable to open folder for name: " + name + ". Not Found: data/" + name)
	}

	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Profile.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "Lists" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Show.json" {
			content ^= byte(0b00000100)
		} else if anElem.Name() == "Embedded" {
			content ^= byte(0b00001000)
		} else {
			return 0, errors.New("Unknow Content: \033[33m" + name + "/" + anElem.Name() + "\033[0m")
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
func CheckListFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name + "/Lists")
	if err != nil {
		return 0, errors.New("Unable to open list folder for name: " + name + ". Not Found: data/" + name + "/Lists")
	}
	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Blacklist.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "History.json" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Whitelist.json" {
			content ^= byte(0b00000100)
		} else {
			return 0, errors.New("Unknow Content: \033[33m" + name + "/" + anElem.Name() + "\033[0m")
		}
	}
	return content, nil
}

// Verify the content of a Embedded folder
// It check if the following files are available:
// data/name/Lists:	Box.json
//
// After reading the Embedded folder, it stores inside a BIT the finded elements in the format:
// BIT format:	0b00000001 -> Box.json file
//
// Print a message when finding an unknown content, with the name in yellow
func CheckEmbeddedFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name + "/Embedded")
	if err != nil {
		return 0, errors.New("Unable to open Embedded folder for name: " + name + ". Not Found: data/" + name + "/Embedded")
	}
	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Box.json" {
			content ^= byte(0b00000001)
		} else {
			return 0, errors.New("Unknow Content: \033[33m" + name + "/" + anElem.Name() + "\033[0m")
		}
	}
	return content, nil
}
