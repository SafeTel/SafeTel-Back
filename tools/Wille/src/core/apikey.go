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
// If ApiKey == defaultValue, then ApiKey is not valid
// If ApiKey != defaultValue, then ApiKey is valid
func (wille *Wille) isValidApiKey() bool {
	if wille.ApiKey == "" {
		return false
	}
	return true
}

// Check if the ApiKey exist on the server.
// If ApiKey is on storage, then ApiKey is valid
func (wille *Wille) CheckApiKeyValidity(name string) error {
	apiKeyCollection := wille.DBForApiKey.Collection("ApiKeyLog")
	filter := bson.M{"apiKey": name}
	isOnStorage, err := utils.IsDataOnStorage(apiKeyCollection, filter)

	if err != nil {
		return err
	} else if isOnStorage {
		return nil
	}
	return nil
}

// ApiKey command
// Assign the value to Wille's ApiKey var
func (wille *Wille) apikey(key string) error {
	// Check if the apikey is a valid one
	if err := wille.CheckApiKeyValidity(key); err != nil {
		return errors.New("ApiKey Not Valid")
	}
	wille.ApiKey = key

	return nil
}
