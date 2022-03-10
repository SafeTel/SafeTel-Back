//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"errors"

	"go.mongodb.org/mongo-driver/bson"
)

func (wille *Wille) checkProfileDataValidity(name string) error {
	s, err := wille.JsonWorker.openAndUnmarshalJson("data/" + name + "/Profile.json")

	if err != nil {
		return err
	}
	keys := []string{
		"email",
		"userName",
		"password",
		"customerInfos",
		"localization",
		"guid",
		"role"}

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
	filter := bson.M{"email": s["email"], "guid": s["guid"]}
	err = wille.JsonWorker.checkDataValidity(wille.User, filter)

	if err != nil {
		return err
	}
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
