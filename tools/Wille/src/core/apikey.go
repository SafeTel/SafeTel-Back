//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"errors"

	utils "PostmanDbDataImplementation/core/Utils"

	"go.mongodb.org/mongo-driver/bson"
)

// Api Key as to be set using command --apikey
// The ApiKey is only assignable by calling the command apikey
// The ApiKey is only assign if it's a valid one, then:
//
// 	If ApiKey == defaultValue, then ApiKey is not valid because the apikey command has not been called
//
// 	If ApiKey != defaultValue, then ApiKey is valid
//
func (wille *Wille) isValidApiKey() bool {
	if wille.ApiKey == "" {
		return false
	}
	return true
}

// Check if the ApiKey exist on the server.
//
// 	If ApiKey is on storage, then ApiKey is valid
//
func (wille *Wille) CheckApiKeyValidity(name string) error {
	apiKeyCollection := wille.DBForApiKey.Collection("ApiKeyLog")
	filter := bson.M{"apiKey": name}
	isOnStorage, err := utils.IsDataOnStorage(apiKeyCollection, filter)

	if err != nil {
		return err
	} else if isOnStorage {
		return nil
	}
	return errors.New("ApiKey Does not exist")
}

// ApiKey command
// Assign the value to Wille's ApiKey var
// The Apikey is only set if it's a valid one
func (wille *Wille) apikey(key string) error {
	// Check if the apikey is a valid one
	if err := wille.CheckApiKeyValidity(key); err != nil {
		return errors.New("ApiKey Not Valid")
	}
	wille.ApiKey = key

	return nil
}
