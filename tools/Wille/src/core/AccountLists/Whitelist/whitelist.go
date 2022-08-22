//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package whitelist

import (
	// Read Json

	utils "PostmanDbDataImplementation/core/Utils"
	// Show Command
	print "PostmanDbDataImplementation/core/Utils/Print"
	// Error Type
	"errors"
	// Mongo Type
	"go.mongodb.org/mongo-driver/mongo"
)

type Whitelist struct {
	Client              *mongo.Client
	DB                  *mongo.Database
	WhitelistCollection *mongo.Collection
	Print               *print.Print
	Config              *utils.Config
	Data                *Data
}

type Data struct {
	PhoneNumbers []string `json:"PhoneNumbers"`
}

// Check the content of a Whitelist object
func (whitelist *Whitelist) checkWhitelistObjectDataValidity(name string, data Data) error {
	for _, phonenumber := range data.PhoneNumbers {
		if phonenumber == "" {
			return errors.New("Problem with json file " + name + "/Lists/Whitelist.jsonBox Missing Whitelist PhoneNumber value")
		}
	}
	return nil
}

// Check the content of the Whitelist.json file and check if the data has not been uploaded yet
func (whitelist *Whitelist) checkWhitelistDataValidity(name string) (Data, error) {
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

func (whitelist *Whitelist) setData(name string) error {
	data, err := whitelist.checkWhitelistDataValidity(name)

	if err != nil {
		return err
	}
	whitelist.Data = &data
	return nil
}

func (whitelist *Whitelist) LoadData(name string) error {
	return whitelist.setData(name)
}

// // Upload the Whitelist.json file
// func (whitelist *Whitelist) UploadWhitelistFile(name string) error {
// 	data, err := whitelist.checkDataValidity(name)
// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace start
// 	// Generating a bson filter using the value of guid
// 	filter := bson.M{"guid": data.Guid}
// 	if err = utils.CheckDataNotExistInCollection(whitelist.WhitelistCollection, filter); err != nil {
// 		whitelist.Print.Info("Whitelist.json data of model " + name + " already exist inside the server")
// 		return nil
// 	}
// 	// Upload
// 	err, inOut, inErr := mongoUtils.Import(whitelist.DEV_URI_USERS_DB, "Whitelist", "data/"+name+"/Lists/Whitelist.json")

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace end
// 	whitelist.Print.Info("StdOut: Uploading the whitelist file of " + name + ": " + inOut)
// 	whitelist.Print.Info("StdErr: Uploading the whitelist file of " + name + ": " + inErr)
// 	return nil
// }

func (whitelist *Whitelist) ShowWhitelist() {
	whitelist.Print.ResetTabForPrint()
	whitelist.Print.Info("\t- Whitelist.json Content:")
	// Print Data
	whitelist.Print.DefinedKeyWithValueWithTab("PhoneNumbers", whitelist.Data.PhoneNumbers)
}

func New(client *mongo.Client, print *print.Print, config *utils.Config) (*Whitelist, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}
	whitelist := Whitelist{Client: client}
	whitelist.DB = whitelist.Client.Database("Melchior")
	whitelist.WhitelistCollection = whitelist.DB.Collection("Whitelist")
	whitelist.Print = print
	whitelist.Config = config
	whitelist.Data = nil

	return &whitelist, nil
}
