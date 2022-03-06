//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/cmd/WILLE/errors"
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"
)

// Domain Layer - Core Functionalities

func (wille *Wille) uploadBlacklistFile(name string) error {
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "Blacklist", "Data/"+name+"/List/Blacklist.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}

	InfoLogger.Println("StdOut: Uploading the blacklist file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the blacklist file of ", name, ": ", inErr)

	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkBlacklistJsonContent(name string) error {
	jsonFile, err := os.Open("Data/" + name + "/List/Blacklist.json")

	if err != nil {
		return err
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return err
	}
	var s map[string]interface{}

	err = json.Unmarshal([]byte(byteValue), &s)
	if err != nil {
		return err
	}
	identifiers := []string{
		"guid",
		"PhoneNumbers"}

	err = wille.checkJsonContent(s, identifiers, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/List/Blacklist.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer
