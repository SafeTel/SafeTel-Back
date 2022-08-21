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

	print "PostmanDbDataImplementation/core/Utils/Print"
)

type Box struct {
	Client        *mongo.Client
	DB            *mongo.Database
	BoxCollection *mongo.Collection
	Print         *print.Print
	Data          *Data
}

type Data struct {
	Boxes []struct {
		BoxId    string `json:"boxid"`
		Activity bool   `json:"activity"`
		Severity string `json:"severity"`
	}
}

// Check the content of a Box object
func (box *Box) checkBoxObjectDataValidity(name string, data Data) error {
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

func (box *Box) setData(name string) error {
	data, err := box.checkBoxDataValidity(name)

	if err != nil {
		return err
	}
	box.Data = &data
	return nil
}

func (box *Box) LoadData(name string) error {
	return box.setData(name)
}

// // Upload the Box.json file
// func (box *Box) UploadBoxFile(name string) error {
// 	data, err := box.checkBoxDataValidity(name)

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace start
// 	// Generating a bson filter using the value of guid
// 	filter := bson.M{"guid": data.Guid}
// 	if err = utils.CheckDataNotExistInCollection(box.BoxCollection, filter); err != nil {
// 		box.Print.Info("Box.json data of model " + name + " already exist inside the server")
// 		return nil
// 	}
// 	// Upload
// 	err, inOut, inErr := mongoUtils.Import(box.DEV_URI_BOXES_DB, "Boxes", "data/"+name+"/Embedded/Box.json")

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace end
// 	box.Print.Info("StdOut: Uploading the box file of " + name + ": " + inOut)
// 	box.Print.Info("StdErr: Uploading the box file of " + name + ": " + inErr)
// 	return nil
// }

func (box *Box) ShowBox() {

	box.Print.ResetTabForPrint()
	box.Print.Info("\t- Box.json Content:")
	box.Print.DefinedKeyWithValueWithTab("Boxes", box.Data.Boxes)
	box.Print.AddOneTabForPrint()
	for index, aBox := range box.Data.Boxes {
		box.Print.InfoWithTab("Box number " + strconv.Itoa(index))
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.BoxId)
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.Activity)
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.Severity)
	}
	box.Print.ResetTabForPrint()

}

func New(client *mongo.Client, print *print.Print, config *utils.Config) (*Box, error) {
	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	} else if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	box := Box{Client: client}
	box.DB = box.Client.Database(config.DEV_DB_BOXES_NAME)
	box.BoxCollection = box.DB.Collection("Boxes")
	box.Print = print

	return &box, nil
}
