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

// Domain Layer - Core Functionalities

func (wille *Wille) checkHistoryDataValidity(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"History"}

	err = wille.checkJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	filter := bson.M{"guid": s["guid"]}
	// keys := []string{"guid"}
	err = wille.checkDataValidity(wille.History, filter)

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

// Repository Layer - Error Checking

func (wille *Wille) checkAndShowHistoryJsonContent(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Lists/History.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"History"}

	err = wille.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer
