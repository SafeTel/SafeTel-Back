//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"os"
)

type ShowJson struct {
	Infos string `json:"infos"`
	Pwd   string `json:"password"`
}

// Domain Layer - Core Functionalities

// Repository Layer - Error Checking

func (wille *Wille) checkShowJsonContent(name string) error {
	jsonFile, err := os.Open("Data/" + name + "/Show.json")

	if err != nil {
		return err
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return err
	}
	var s map[string]interface{}

	err = json.Unmarshal([]byte(byteValue), &s)
	if err != nil {
		return err
	}
	identifiers := []string{
		"infos",
		"password"}

	err = wille.checkJsonContent(s, identifiers, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Show.json" + ": " + err.Error())
	}
	return nil
}

// Repository Layer

func (wille *Wille) printShowJsonFile(name string) error {
	return nil
}
