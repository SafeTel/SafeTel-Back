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

type Call struct {
	Number string `json:"number"`
	Status string `json:"status"`
	Time   int    `json:"time"`
}

type History struct {
	Guid  string `json:"guid"`
	Calls []Call `json:"History"`
}

// Check the content of a History object
func (wille *Wille) checkHistoryObjectDataValidity(name string, history History) error {
	if history.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/History.json" + ": Missing History Guid value")
	}
	for _, call := range history.Calls {
		if call.Number == "" {
			return errors.New("Problem with json file " + name + "/Lists/History.json" + ": Missing History Call Number value")
		} else if call.Status != "Missed" || call.Status != "Received" || call.Status != "Blocked" || call.Status != "Outgoing" {
			return errors.New("Problem with json file " + name + "/Lists/History.json" + ": Missing History Call status value")
		}
	}
	return nil
}

// Check the content of the History.json file and check if the data has not been uploaded yet
func (wille *Wille) checkHistoryDataValidity(name string) (History, error) {
	jsonFile, err := os.Open("data/" + name + "/Lists/History.json")

	if err != nil {
		return History{}, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return History{}, err
	}
	var history History

	decoder := json.NewDecoder(bytes.NewReader(byteValue))
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&history); err != nil {
		return History{}, err
	}

	// check Json Content
	if err = wille.checkHistoryObjectDataValidity(name, history); err != nil {
		return History{}, err
	}

	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": history.Guid}
	if err = wille.checkDataValidityOnStorage(wille.History, filter); err != nil {
		return History{}, err
	}
	return history, nil
}

// Upload the History.json file
func (wille *Wille) uploadHistoryFile(name string) error {
	if _, err := wille.checkHistoryDataValidity(name); err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "History", "data/"+name+"/Lists/History.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the history file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the history file of ", name, ": ", inErr)
	return nil
}

func (wille *Wille) ShowHistory(history History) {
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "Guid", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, history.Guid, ResetColor)
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, "PhoneNumbers", ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, history.Calls, ResetColor)
}

// Check the content of the Blacklist.json file and print it
func (wille *Wille) checkAndShowHistoryJsonContent(name string) error {
	history, err := wille.checkHistoryDataValidity(name)
	if err != nil {
		return err
	}

	wille.ShowHistory(history)
	return nil
}
