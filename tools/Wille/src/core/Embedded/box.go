//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// box.go
//

package box

import (
	"errors"
	"strconv"

	"go.mongodb.org/mongo-driver/mongo"

	utils "PostmanDbDataImplementation/core/Utils"

	mongoUtils "PostmanDbDataImplementation/core/Utils/Mongo"
	print "PostmanDbDataImplementation/core/Utils/Print"

	"go.mongodb.org/mongo-driver/bson"
)

type Box struct {
	Client            *mongo.Client
	DB                *mongo.Database
	BoxCollection     *mongo.Collection
	Print             *print.Print
	DEV_DB_BOXES_NAME string
	DEV_URI_USERS_DB  string
}

type Data struct {
	Guid  string `json:"guid"`
	Boxes []struct {
		BoxId    string `json:"boxid"`
		Activity bool   `json:"activity"`
		Severity string `json:"severity"`
	}
}

// Check the content of a Box object
func (box *Box) checkBoxObjectDataValidity(name string, data Data) error {
	if data.Guid == "" {
		return errors.New("Problem with json file " + name + "/Embedded/Box.json: Missing Box Guid value")
	}
	for _, aBox := range data.Boxes {
		if aBox.BoxId == "" {
			return errors.New("Problem with json file " + name + "/Embedded/Box.json: Missing BoxId value")
		} else if aBox.Severity == "" {
			return errors.New("Problem with json file " + name + "/Embedded/Box.json: Missing Severity value")
		}
	}
	return nil
}

// Check the content of the Box.json file and check if the data has not been uploaded yet
func (box *Box) checkBoxDataValidity(name string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Embedded/Box.json")
	if err != nil {
		return Data{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&data); err != nil {
		return Data{}, err
	}
	// check Json Content
	if err = box.checkBoxObjectDataValidity(name, data); err != nil {
		return Data{}, err
	}
	return data, nil
}

// Upload the Box.json file
func (box *Box) UploadBoxFile(name string) error {
	data, err := box.checkBoxDataValidity(name)

	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": data.Guid}
	if err = utils.CheckDataValidityOnStorage(box.BoxCollection, filter); err != nil {
		box.Print.Info("Box.json data of model " + name + " already exist inside the server")
		return nil
	}
	// Upload
	err, inOut, inErr := mongoUtils.Import(box.DEV_URI_USERS_DB, "Boxes", "data/"+name+"/Embedded/Box.json")

	if err != nil {
		return err
	}
	box.Print.Info("StdOut: Uploading the box file of " + name + ": " + inOut)
	box.Print.Info("StdErr: Uploading the box file of " + name + ": " + inErr)
	return nil
}

func (box *Box) showBox(data Data) {
	box.Print.DefinedKeyWithValueWithTab("Guid", data.Guid)
	box.Print.DefinedKeyWithValueWithTab("Boxes", data.Boxes)

	box.Print.AddOneTabForPrint()
	for index, aBox := range data.Boxes {
		box.Print.InfoWithTab("Box number " + strconv.Itoa(index))
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.BoxId)
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.Activity)
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.Severity)
	}
	box.Print.ResetTabForPrint()

}

// Check the content of the Box.json file and print it
func (box *Box) CheckAndShowBoxJsonContent(name string) error {
	data, err := box.checkBoxDataValidity(name)
	if err != nil {
		return err
	}

	box.showBox(data)
	return nil
}

func New(client *mongo.Client, print *print.Print) (*Box, error) {
	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	} else if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	box := Box{Client: client}
	box.DEV_DB_BOXES_NAME = config.DEV_DB_BOXES_NAME
	box.DEV_URI_USERS_DB = config.DEV_URI_USERS_DB

	box.DB = box.Client.Database(box.DEV_DB_BOXES_NAME)

	box.BoxCollection = box.DB.Collection("Boxes")
	box.Print = print

	return &box, nil
}
