//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"bytes"
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"

	input "PostmanDbDataImplementation/errors"

	"go.mongodb.org/mongo-driver/bson"
)

type Blacklist struct {
	Guid         string   `json:"guid"`
	PhoneNumbers []string `json:"PhoneNumbers"`
}

func (wille *Wille) checkBlacklistObjectDataValidity(name string, blacklist Blacklist) error {
	if blacklist.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Blacklist.json" + ": Missing Blacklist Guid value")
	}

	for _, phonenumber := range blacklist.PhoneNumbers {
		if phonenumber == "" {
			return errors.New("Problem with json file " + name + "/Lists/Blacklist.json" + ": Missing Blacklist Guid value")
		}
	}
	return nil
}

// Check the content of the Blacklist.json file and check if the data has not been uploaded yet
func (wille *Wille) checkBlacklistDataValidity(name string) (Blacklist, error) {
	jsonFile, err := os.Open("data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return Blacklist{}, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return Blacklist{}, err
	}
	var blacklist Blacklist

	decoder := json.NewDecoder(bytes.NewReader(byteValue))
	decoder.DisallowUnknownFields()

	if err = decoder.Decode(&blacklist); err != nil {
		return Blacklist{}, err
	}

	// check Json Content

	if err = wille.checkBlacklistObjectDataValidity(name, blacklist); err != nil {
		return Blacklist{}, err
	}

	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": blacklist.Guid}
	err = wille.checkDataValidityOnStorage(wille.Blacklist, filter)

	if err != nil {
		return Blacklist{}, err
	}

	return blacklist, nil

}

// Upload the Blacklist.json file
func (wille *Wille) uploadBlacklistFile(name string) error {
	if _, err := wille.checkBlacklistDataValidity(name); err != nil {
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

func (wille *Wille) ShowBlacklist(blacklist Blacklist) {
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "Guid", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, blacklist.Guid, ResetColor)
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "PhoneNumbers", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, blacklist.PhoneNumbers, ResetColor)
}

// Check the content of the Blacklist.json file and print it
func (wille *Wille) checkAndShowBlacklistJsonContent(name string) error {
	blacklist, err := wille.checkBlacklistDataValidity(name)
	if err != nil {
		return err
	}

	wille.ShowBlacklist(blacklist)
	return nil
}
