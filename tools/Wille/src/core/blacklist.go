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

// Domain Layer - Core Functionalities

func (wille *Wille) checkBlacklistDataValidity(name string) error {
	s, err := wille.openAndUnmarshalJson("Data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return err
	}
	filter := bson.M{"guid": s["guid"]}
	// keys := []string{"guid"}
	err = wille.checkDataValidity(wille.Blacklist, filter)

	if err != nil {
		return err
	}
	return nil
}

func (wille *Wille) uploadBlacklistFile(name string) error {
	err := wille.checkBlacklistDataValidity(name)

	if err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "Blacklist", "Data/"+name+"/Lists/Blacklist.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}

	InfoLogger.Println("StdOut: Uploading the blacklist file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the blacklist file of ", name, ": ", inErr)

	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkAndShowBlacklistJsonContent(name string) error {
	s, err := wille.openAndUnmarshalJson("Data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return err
	}
	keys := []string{
		"guid",
		"PhoneNumbers"}

	err = wille.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Lists/Blacklist.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer
