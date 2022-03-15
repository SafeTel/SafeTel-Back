//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/errors"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
)

// Check the content of the History.json file and check if the data has not been uploaded yet
func (wille *Wille) checkHistoryDataValidity(name string) error {
	s, err := wille.JsonReader.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"guid",
		"History"}

	err = wille.JsonReader.checkJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": s["guid"]}
	// keys := []string{"guid"}
	err = wille.JsonReader.checkDataValidity(wille.History, filter)

	if err != nil {
		return err
	}
	return nil
}

// Upload the History.json file
func (wille *Wille) uploadHistoryFile(name string) error {
	err := wille.checkHistoryDataValidity(name)

	if err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "History", "data/"+name+"/Lists/History.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}

	InfoLogger.Println("StdOut: Uploading the history file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the history file of ", name, ": ", inErr)

	return nil
}

// Check the content of the Blacklist.json file and print it
func (wille *Wille) checkAndShowHistoryJsonContent(name string) error {
	s, err := wille.JsonReader.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"guid",
		"History"}

	err = wille.JsonReader.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	return nil
}
