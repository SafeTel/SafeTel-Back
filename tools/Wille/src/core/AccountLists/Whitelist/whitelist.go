//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package whitelist

import (
	utils "PostmanDbDataImplementation/core/Utils"
	mongoUtils "PostmanDbDataImplementation/core/Utils/Mongo"
	print "PostmanDbDataImplementation/core/Utils/Print"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type Whitelist struct {
	Client              *mongo.Client
	DB                  *mongo.Database
	WhitelistCollection *mongo.Collection
	Print               *print.Print
	DEV_DB_USERS_NAME   string
	DEV_URI_USERS_DB    string
}

type Data struct {
	Guid         string   `json:"guid"`
	PhoneNumbers []string `json:"PhoneNumbers"`
}

// Check the content of a Whitelist object
func (whitelist *Whitelist) checkWhitelistObjectDataValidity(name string, data Data) error {
	if data.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Whitelist.jsonBox Missing Whitelist Guid value")
	}
	for _, phonenumber := range data.PhoneNumbers {
		if phonenumber == "" {
			return errors.New("Problem with json file " + name + "/Lists/Whitelist.jsonBox Missing Whitelist PhoneNumber value")
		}
	}
	return nil
}

// Check the content of the Whitelist.json file and check if the data has not been uploaded yet
func (whitelist *Whitelist) checkDataValidity(name string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Lists/Whitelist.json")
	if err != nil {
		return Data{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&data); err != nil {
		return Data{}, err
	}
	// check Json Content
	if err = whitelist.checkWhitelistObjectDataValidity(name, data); err != nil {
		return Data{}, err
	}
	return data, nil
}

// Upload the Whitelist.json file
func (whitelist *Whitelist) UploadWhitelistFile(name string) error {
	data, err := whitelist.checkDataValidity(name)
	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": data.Guid}
	if err = utils.CheckDataNotExitInCollection(whitelist.WhitelistCollection, filter); err != nil {
		whitelist.Print.Info("Whitelist.json data of model " + name + " already exist inside the server")
		return nil
	}
	// Upload
	err, inOut, inErr := mongoUtils.Import(whitelist.DEV_URI_USERS_DB, "Whitelist", "data/"+name+"/Lists/Whitelist.json")

	if err != nil {
		return err
	}
	whitelist.Print.Info("StdOut: Uploading the whitelist file of " + name + ": " + inOut)
	whitelist.Print.Info("StdErr: Uploading the whitelist file of " + name + ": " + inErr)
	return nil
}

func (whitelist *Whitelist) showWhitelist(data Data) {
	whitelist.Print.DefinedKeyWithValueWithTab("Guid", data.Guid)
	whitelist.Print.DefinedKeyWithValueWithTab("PhoneNumbers", data.PhoneNumbers)
}

// Check the content of the Whitelist.json file and print it
func (whitelist *Whitelist) CheckAndShowWhitelistJsonContent(name string) error {
	data, err := whitelist.checkDataValidity(name)
	if err != nil {
		return err
	}

	whitelist.showWhitelist(data)
	return nil
}

func New(client *mongo.Client, print *print.Print) (*Whitelist, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}
	whitelist := Whitelist{Client: client}
	whitelist.DB = whitelist.Client.Database("Melchior")
	whitelist.WhitelistCollection = whitelist.DB.Collection("Whitelist")
	whitelist.Print = print
	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	}
	whitelist.DEV_DB_USERS_NAME = config.DEV_DB_USERS_NAME
	whitelist.DEV_URI_USERS_DB = config.DEV_URI_USERS_DB

	return &whitelist, nil
}
