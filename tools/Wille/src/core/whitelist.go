//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	input "PostmanDbDataImplementation/errors"
	"errors"

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
	var whitelist Whitelist

	decoder, err := wille.JsonReader.openAndGenerateJsonDecoder("data/" + name + "/Lists/Blacklist.json")
	if err != nil {
		return Whitelist{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&whitelist); err != nil {
		return Whitelist{}, err
	}
	// check Json Content
	if err = wille.checkWhitelistObjectDataValidity(name, whitelist); err != nil {
		return Whitelist{}, err
	}
	return whitelist, nil
}

// Upload the Whitelist.json file
func (wille *Wille) uploadWhitelistFile(name string) error {
	whitelist, err := wille.checkWhitelistDataValidity(name)
	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": whitelist.Guid}
	if err = wille.checkDataValidityOnStorage(wille.Whitelist, filter); err != nil {
		return err
	}
	// Upload
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "Whitelist", "data/"+name+"/Lists/Whitelist.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the whitelist file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the whitelist file of ", name, ": ", inErr)
	return nil
}

func (wille *Wille) showWhitelist(whitelist Whitelist) {
	wille.printDefinedKeyWithValue("Guid", whitelist.Guid)
	wille.printDefinedKeyWithValue("PhoneNumbers", whitelist.PhoneNumbers)
}

// Check the content of the Whitelist.json file and print it
func (wille *Wille) checkAndShowWhitelistJsonContent(name string) error {
	whitelist, err := wille.checkWhitelistDataValidity(name)
	if err != nil {
		return err
	}

	wille.showWhitelist(whitelist)
	return nil
}
