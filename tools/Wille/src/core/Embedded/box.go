//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// box.go
//

package box

import (
	"context"
	"errors"
	"strconv"
	"time"

	utils "PostmanDbDataImplementation/core/Utils"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"

	print "PostmanDbDataImplementation/core/Utils/Print"
)

type Box struct {
	Client                 *mongo.Client
	DB                     *mongo.Database
	BoxCollection          *mongo.Collection
	UnclaimedBoxCollection *mongo.Collection
	Print                  *print.Print
	Config                 *utils.Config
	Data                   *Data
}

type Data struct {
	Boxes []struct {
		BoxId string `json:"boxid"`
	}
}

// Check the content of a Box object
func (box *Box) checkBoxObjectDataValidity(name string, data Data) error {
	for _, aBox := range data.Boxes {
		if aBox.BoxId == "" {
			return errors.New("Problem with json file " + name + "/Embedded/Box.json: Missing BoxId value")
		}
	}
	return nil
}

// Check the content of the Box.json file and check if the data has not been uploaded yet
func (box *Box) checkBoxDataValidity(name string, filepath string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder(filepath)
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

// Loading a File

func (box *Box) setDataFile(filePath string) error {
	data, err := box.checkBoxDataValidity(filePath, filePath)

	if err != nil {
		return err
	}
	box.Data = &data
	return nil
}

func (box *Box) LoadFile(filePath string) error {
	return box.setDataFile(filePath)
}

// Loading a Model

func (box *Box) setData(name string) error {
	data, err := box.checkBoxDataValidity(name, "data/"+name+"/Embedded/Box.json")

	if err != nil {
		return err
	}
	box.Data = &data
	return nil
}

func (box *Box) LoadData(name string) error {
	return box.setData(name)
}

// Upload the Box.json file
func (box *Box) InsertBoxes(name string) error {
	for _, aBox := range box.Data.Boxes {
		// Generating a bson filter using the value of guid
		filter := bson.M{"boxid": aBox.BoxId}

		if err := utils.CheckDataNotExistInCollection(box.UnclaimedBoxCollection, filter); err != nil {
			box.Print.Info("Box.json data of model " + name + " already exist inside the server")
			continue
		}
		// Insert Boxes
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		_, err := box.UnclaimedBoxCollection.InsertOne(ctx, bson.D{
			{Key: "boxid", Value: aBox.BoxId},
		})

		if err != nil {
			return err
		}
	}

	return nil
}

func (box *Box) ShowBox() {
	box.Print.ResetTabForPrint()
	box.Print.Info("\t- Box.json Content:")
	box.Print.DefinedKeyWithValueWithTab("Boxes", box.Data.Boxes)
	box.Print.AddOneTabForPrint()
	for index, aBox := range box.Data.Boxes {
		box.Print.InfoWithTab("Box number " + strconv.Itoa(index))
		box.Print.DefinedKeyWithValueWithTab("Box", aBox.BoxId)
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
	box.UnclaimedBoxCollection = box.DB.Collection("UnclaimedBoxes")
	box.Print = print
	box.Config = config

	return &box, nil
}
