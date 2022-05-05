//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package blacklist

import (
	"errors"

	"go.mongodb.org/mongo-driver/mongo"

	utils "PostmanDbDataImplementation/core/Utils"

	mongoUtils "PostmanDbDataImplementation/core/Utils/Mongo"
	print "PostmanDbDataImplementation/core/Utils/Print"

	"go.mongodb.org/mongo-driver/bson"
)

type Blacklist struct {
	Client              *mongo.Client
	DB                  *mongo.Database
	BlacklistCollection *mongo.Collection
	Print               *print.Print
	DEV_DB_USERS_NAME   string
	DEV_URI_USERS_DB    string
}

type Data struct {
	Guid         string   `json:"guid"`
	PhoneNumbers []string `json:"PhoneNumbers"`
}

// Check the content of a Blacklist object
func (blacklist *Blacklist) checkBlacklistObjectDataValidity(name string, data Data) error {
	if data.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Blacklist.jsonBox Missing Blacklist Guid value")
	}
	for _, phonenumber := range data.PhoneNumbers {
		if phonenumber == "" {
			return errors.New("Problem with json file " + name + "/Lists/Blacklist.jsonBox Missing Blacklist PhoneNumber value")
		}
	}
	return nil
}

// Check the content of the Blacklist.json file and check if the data has not been uploaded yet
func (blacklist *Blacklist) checkBlacklistDataValidity(name string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Lists/Blacklist.json")
	if err != nil {
		return Data{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&data); err != nil {
		return Data{}, err
	}
	// check Json Content
	if err = blacklist.checkBlacklistObjectDataValidity(name, data); err != nil {
		return Data{}, err
	}
	return data, nil
}

// Upload the Blacklist.json file
func (blacklist *Blacklist) UploadBlacklistFile(name string) error {
	data, err := blacklist.checkBlacklistDataValidity(name)

	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": data.Guid}
	if err = utils.CheckDataNotExitInCollection(blacklist.BlacklistCollection, filter); err != nil {
		blacklist.Print.Info("Blacklist.json data of model " + name + " already exist inside the server")
		return nil
	}
	// Upload
	err, inOut, inErr := mongoUtils.Import(blacklist.DEV_URI_USERS_DB, "Blacklist", "data/"+name+"/Lists/Blacklist.json")

	if err != nil {
		return err
	}
	blacklist.Print.Info("StdOut: Uploading the blacklist file of " + name + ": " + inOut)
	blacklist.Print.Info("StdErr: Uploading the blacklist file of " + name + ": " + inErr)
	return nil
}

func (blacklist *Blacklist) showBlacklist(data Data) {
	blacklist.Print.DefinedKeyWithValueWithTab("Guid", data.Guid)
	blacklist.Print.DefinedKeyWithValueWithTab("PhoneNumbers", data.PhoneNumbers)
}

// Check the content of the Blacklist.json file and print it
func (blacklist *Blacklist) CheckAndShowBlacklistJsonContent(name string) error {
	data, err := blacklist.checkBlacklistDataValidity(name)
	if err != nil {
		return err
	}

	blacklist.showBlacklist(data)
	return nil
}

func New(client *mongo.Client, print *print.Print) (*Blacklist, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	blacklist := Blacklist{Client: client}
	blacklist.DB = blacklist.Client.Database("Melchior")
	blacklist.BlacklistCollection = blacklist.DB.Collection("Blacklist")
	blacklist.Print = print
	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	}
	blacklist.DEV_DB_USERS_NAME = config.DEV_DB_USERS_NAME
	blacklist.DEV_URI_USERS_DB = config.DEV_URI_USERS_DB

	return &blacklist, nil
}
