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

func (wille *Wille) checkWhitelistDataValidity(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Lists/Whitelist.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"PhoneNumbers"}
	err = wille.checkJsonContent(s, keys, nil)

	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/Whitelist.json" + ": " + err.Error())
	}
	filter := bson.M{"guid": s["guid"]}
	err = wille.checkDataValidity(wille.Whitelist, filter)

	if err != nil {
		return err
	}
	return nil
}

func (wille *Wille) uploadWhitelistFile(name string) error {
	err := wille.checkWhitelistDataValidity(name)

	if err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "Whitelist", "data/"+name+"/Lists/Whitelist.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the whitelist file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the whitelist file of ", name, ": ", inErr)

	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkAndShowWhitelistJsonContent(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Lists/Whitelist.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"PhoneNumbers"}

	err = wille.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/Whitelist.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer
