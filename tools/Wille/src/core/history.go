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

func (wille *Wille) checkHistoryDataValidity(name string) error {
	s, err := wille.JsonWorker.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"History"}

	err = wille.JsonWorker.checkJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	filter := bson.M{"guid": s["guid"]}
	// keys := []string{"guid"}
	err = wille.JsonWorker.checkDataValidity(wille.History, filter)

	if err != nil {
		return err
	}
	return nil
}

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
	s, err := wille.JsonWorker.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"guid",
		"History"}

	err = wille.JsonWorker.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	return nil
}
