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
	var history History

	decoder, err := wille.JsonReader.openAndGenerateJsonDecoder("data/" + name + "/Lists/History.json")
	if err != nil {
		return History{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&history); err != nil {
		return History{}, err
	}

	// check Json Content
	if err = wille.checkHistoryObjectDataValidity(name, history); err != nil {
		return History{}, err
	}
	return history, nil
}

// Upload the History.json file
func (wille *Wille) uploadHistoryFile(name string) error {
	history, err := wille.checkHistoryDataValidity(name)

	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"guid": history.Guid}
	if err = wille.checkDataValidityOnStorage(wille.History, filter); err != nil {
		return err
	}
	// Upload
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "History", "data/"+name+"/Lists/History.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the history file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the history file of ", name, ": ", inErr)
	return nil
}

func (wille *Wille) showHistory(history History) {
	wille.printDefinedKeyWithValue("Guid", history.Guid)
	wille.printDefinedKeyWithValue("Calls", history.Calls)
	wille.addOneTabForPrint()
	for index, call := range history.Calls {
		wille.print("Call number " + string(index))
		wille.printDefinedKeyWithValue("Call", call.Number)
		wille.printDefinedKeyWithValue("Call", call.Status)
		wille.printDefinedKeyWithValue("Call", call.Time)
	}
	wille.resetTabForPrint()
}

// Check the content of the Blacklist.json file and print it
func (wille *Wille) checkAndShowHistoryJsonContent(name string) error {
	history, err := wille.checkHistoryDataValidity(name)
	if err != nil {
		return err
	}

	wille.showHistory(history)
	return nil
}
