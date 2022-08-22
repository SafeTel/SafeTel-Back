//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package history

import (
	// Read Json
	utils "PostmanDbDataImplementation/core/Utils"
	// Show command
	print "PostmanDbDataImplementation/core/Utils/Print"
	// Itoa Function
	"strconv"
	// Error Type
	"errors"
	// Mongo Type
	"go.mongodb.org/mongo-driver/mongo"
)

type History struct {
	Client            *mongo.Client
	DB                *mongo.Database
	HistoryCollection *mongo.Collection
	Print             *print.Print
	Config            *utils.Config
	Data              *Data
}

type Call struct {
	Number string `json:"number"`
	Status string `json:"status"`
	Time   int    `json:"time"`
}

type Data struct {
	Calls []Call `json:"History"`
}

// Check the content of a History object
func (history *History) checkHistoryObjectDataValidity(name string, data Data) error {
	for _, call := range data.Calls {
		if call.Number == "" {
			return errors.New("Problem with json file " + name + "/Lists/History.jsonBox Missing History Call Number value")
		} else if call.Status != "Missed" && call.Status != "Received" && call.Status != "Blocked" && call.Status != "Outgoing" {
			return errors.New("Problem with json file " + name + "/Lists/History.jsonBox Missing History Call status value")
		}
	}
	return nil
}

// Check the content of the History.json file and check if the data has not been uploaded yet
func (history *History) checkHistoryDataValidity(name string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Lists/History.json")
	if err != nil {
		return Data{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&data); err != nil {
		return Data{}, err
	}

	// check Json Content
	if err = history.checkHistoryObjectDataValidity(name, data); err != nil {
		return Data{}, err
	}
	return data, nil
}

func (history *History) setData(name string) error {
	data, err := history.checkHistoryDataValidity(name)

	if err != nil {
		return err
	}
	history.Data = &data
	return nil
}

func (history *History) LoadData(name string) error {
	return history.setData(name)
}

// // Upload the History.json file
// func (history *History) UploadHistoryFile(name string) error {
// 	data, err := history.checkHistoryDataValidity(name)

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace start
// 	// Generating a bson filter using the value of guid
// 	filter := bson.M{"guid": data.Guid}
// 	if err = utils.CheckDataNotExistInCollection(history.HistoryCollection, filter); err != nil {
// 		history.Print.Info("History.json data of model " + name + " already exist inside the server")
// 		return nil
// 	}
// 	// Upload
// 	err, inOut, inErr := mongoUtils.Import(history.DEV_URI_USERS_DB, "History", "data/"+name+"/Lists/History.json")

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace end
// 	history.Print.Info("StdOut: Uploading the history file of " + name + ": " + inOut)
// 	history.Print.Info("StdErr: Uploading the history file of " + name + ": " + inErr)
// 	return nil
// }

func (history *History) ShowHistory() {

	history.Print.ResetTabForPrint()
	history.Print.Info("\t- History.json Content:")
	// Print Data
	history.Print.DefinedKeyWithValueWithTab("Calls", history.Data.Calls)
	history.Print.AddOneTabForPrint()
	for index, call := range history.Data.Calls {
		history.Print.InfoWithTab("Call number " + strconv.Itoa(index))
		history.Print.DefinedKeyWithValueWithTab("Call", call.Number)
		history.Print.DefinedKeyWithValueWithTab("Call", call.Status)
		history.Print.DefinedKeyWithValueWithTab("Call", call.Time)
	}
	history.Print.ResetTabForPrint()
}

func New(client *mongo.Client, print *print.Print, config *utils.Config) (*History, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	history := History{Client: client}
	history.DB = history.Client.Database("Melchior")
	history.HistoryCollection = history.DB.Collection("History")
	history.Print = print
	history.Config = config
	history.Data = nil

	return &history, nil
}
