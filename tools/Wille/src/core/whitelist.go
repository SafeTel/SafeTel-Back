//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	input "PostmanDbDataImplementation/errors"
	"bytes"
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"

	"go.mongodb.org/mongo-driver/bson"
)

type Whitelist struct {
	Guid         string   `json:"guid"`
	PhoneNumbers []string `json:"PhoneNumbers"`
}

// Check the content of a Whitelist object
func (wille *Wille) checkWhitelistObjectDataValidity(name string, whitelist Whitelist) error {
	if whitelist.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Whitelist.json" + ": Missing Whitelist Guid value")
	}
	for _, phonenumber := range whitelist.PhoneNumbers {
		if phonenumber == "" {
			return errors.New("Problem with json file " + name + "/Lists/Whitelist.json" + ": Missing Whitelist PhoneNumber value")
		}
	}
	return nil
}

// Check the content of the Whitelist.json file and check if the data has not been uploaded yet
func (wille *Wille) checkWhitelistDataValidity(name string) (Whitelist, error) {
	jsonFile, err := os.Open("data/" + name + "/Lists/Blacklist.json")

	if err != nil {
		return Whitelist{}, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return Whitelist{}, err
	}
	var whitelist Whitelist

	decoder := json.NewDecoder(bytes.NewReader(byteValue))
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&whitelist); err != nil {
		return Whitelist{}, err
	}

	// check Json Content
	if err = wille.checkWhitelistObjectDataValidity(name, whitelist); err != nil {
		return Whitelist{}, err
	}

	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": whitelist.Guid}
	err = wille.checkDataValidityOnStorage(wille.Whitelist, filter)

	if err != nil {
		return Whitelist{}, err
	}
	return whitelist, nil
}

// Upload the Whitelist.json file
func (wille *Wille) uploadWhitelistFile(name string) error {
	if _, err := wille.checkWhitelistDataValidity(name); err != nil {
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

func (wille *Wille) ShowWhitelist(whitelist Whitelist) {
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "Guid", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, whitelist.Guid, ResetColor)
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "PhoneNumbers", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, whitelist.PhoneNumbers, ResetColor)
}

// Check the content of the Whitelist.json file and print it
func (wille *Wille) checkAndShowWhitelistJsonContent(name string) error {
	whitelist, err := wille.checkWhitelistDataValidity(name)
	if err != nil {
		return err
	}

	wille.ShowWhitelist(whitelist)
	return nil
}
