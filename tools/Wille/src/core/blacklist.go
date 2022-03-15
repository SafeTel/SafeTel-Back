//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"errors"

	input "PostmanDbDataImplementation/errors"

	"go.mongodb.org/mongo-driver/bson"
)

// Check the content of the Blacklist.json file and check if the data has not been uploaded yet
func (wille *Wille) checkBlacklistDataValidity(name string) error {
	s, err := wille.JsonReader.openAndUnmarshalJson("data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"guid",
		"PhoneNumbers"}
	err = wille.JsonReader.checkJsonContent(s, keys, nil)

	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/Blacklist.json" + ": " + err.Error())
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": s["guid"]}
	err = wille.JsonReader.checkDataValidity(wille.Blacklist, filter)

	if err != nil {
		return err
	}
	return nil
}

// Upload the Blacklist.json file
func (wille *Wille) uploadBlacklistFile(name string) error {
	err := wille.checkBlacklistDataValidity(name)

	if err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "Blacklist", "data/"+name+"/Lists/Blacklist.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}

	InfoLogger.Println("StdOut: Uploading the blacklist file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the blacklist file of ", name, ": ", inErr)

	return nil
}

// Check the content of the Blacklist.json file and print it
func (wille *Wille) checkAndShowBlacklistJsonContent(name string) error {
	s, err := wille.JsonReader.openAndUnmarshalJson("data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"guid",
		"PhoneNumbers"}

	err = wille.JsonReader.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/Blacklist.json" + ": " + err.Error())
	}
	return nil
}
