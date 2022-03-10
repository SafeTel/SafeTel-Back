//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/errors"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
)

// Check the content of the Profile.json file and check if the data has not been uploaded yet
func (wille *Wille) checkProfileDataValidity(name string) error {
	s, err := wille.JsonWorker.openAndUnmarshalJson("data/" + name + "/Profile.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"email",
		"userName",
		"password",
		"customerInfos",
		"localization",
		"guid",
		"role"}

	// Object keys of element related to basic keys of element of the json object
	objectKeys := []string{
		"firstName",
		"lastName",
		"phoneNumber",
		"country",
		"region",
		"adress"}

	err = wille.JsonWorker.checkJsonContent(s, keys, objectKeys)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Profile.json" + ": " + err.Error())
	}
	// Generating a bson filter using the values of guid and email
	filter := bson.M{"email": s["email"], "guid": s["guid"]}
	err = wille.JsonWorker.checkDataValidity(wille.User, filter)

	if err != nil {
		return err
	}
	return nil
}

// Upload the Profile.json file
func (wille *Wille) uploadProfileFile(name string) error {
	err := wille.checkProfileDataValidity(name)

	if err != nil {
		return err
	}
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "User", "data/"+name+"/Profile.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the profile file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the profile file of ", name, ": ", inErr)

	return nil
}

// Check the content of the Profile.json file and print it
func (wille *Wille) checkAndShowProfileJsonContent(name string) error {
	s, err := wille.JsonWorker.openAndUnmarshalJson("data/" + name + "/Profile.json")

	if err != nil {
		return err
	}
	// Basics keys of elements of the json object
	keys := []string{
		"email",
		"userName",
		"password",
		"customerInfos",
		"localization",
		"guid",
		"role"}

	// Object keys of element related to basic keys of element of the json object
	objectKeys := []string{
		"firstName",
		"lastName",
		"phoneNumber",
		"country",
		"region",
		"adress"}

	err = wille.JsonWorker.checkAndShowJsonContent(s, keys, objectKeys)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Profile.json" + ": " + err.Error())
	}
	return nil
}
