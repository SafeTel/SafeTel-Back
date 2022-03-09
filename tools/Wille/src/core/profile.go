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

// Domain Layer - Core Functionalities

func (wille *Wille) checkProfileDataValidity(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Profile.json")

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

	err = wille.checkJsonContent(s, keys, objectKeys)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Profile.json" + ": " + err.Error())
	}
	filter := bson.M{"email": s["email"], "guid": s["guid"]}
	err = wille.checkDataValidity(wille.User, filter)

	if err != nil {
		return err
	}
	return nil
}

// Repository Layer - Error Checking

func (wille *Wille) checkAndShowProfileJsonContent(name string) error {
	s, err := wille.openAndUnmarshalJson("data/" + name + "/Profile.json")

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

	err = wille.checkAndShowJsonContent(s, keys, objectKeys)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Profile.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer
