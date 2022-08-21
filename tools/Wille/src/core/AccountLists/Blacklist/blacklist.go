//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package blacklist

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

type Blacklist struct {
	Client              *mongo.Client
	DB                  *mongo.Database
	BlacklistCollection *mongo.Collection
	Print               *print.Print
	Data                *Data
}

type Data struct {
	PhoneNumbers []string `json:"PhoneNumbers"`
}

// Check the content of a Blacklist object
func (blacklist *Blacklist) checkBlacklistObjectDataValidity(name string, data Data) error {
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

func (blacklist *Blacklist) setData(name string) error {
	data, err := blacklist.checkBlacklistDataValidity(name)

	if err != nil {
		return err
	}
	blacklist.Data = &data
	return nil
}

func (blacklist *Blacklist) LoadData(name string) error {
	return blacklist.setData(name)
}

// // Upload the Blacklist.json file
// func (blacklist *Blacklist) UploadBlacklistFile(name string) error {
// 	data, err := blacklist.checkBlacklistDataValidity(name)

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace start
// 	// Generating a bson filter using the value of guid
// 	filter := bson.M{"guid": data.Guid}
// 	if err = utils.CheckDataNotExistInCollection(blacklist.BlacklistCollection, filter); err != nil {
// 		blacklist.Print.Info("Blacklist.json data of model " + name + " already exist inside the server")
// 		return nil
// 	}
// 	// Upload
// 	err, inOut, inErr := mongoUtils.Import(blacklist.DEV_URI_USERS_DB, "Blacklist", "data/"+name+"/Lists/Blacklist.json")

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace end
// 	blacklist.Print.Info("StdOut: Uploading the blacklist file of " + name + ": " + inOut)
// 	blacklist.Print.Info("StdErr: Uploading the blacklist file of " + name + ": " + inErr)
// 	return nil
// }

func (blacklist *Blacklist) ShowBlacklist() {
	blacklist.Print.ResetTabForPrint()
	blacklist.Print.Info("\t- Blacklist.json Content:")
	// Print Data
	blacklist.Print.DefinedKeyWithValueWithTab("PhoneNumbers", blacklist.Data.PhoneNumbers)
	blacklist.Print.ResetTabForPrint()
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
	blacklist.Data = nil

	return &blacklist, nil
}
