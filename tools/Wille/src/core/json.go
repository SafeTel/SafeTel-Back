//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"os"
	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
)

func OpenAndGenerateJsonDecoder(file string) (*json.Decoder, error) {
	jsonFile, err := os.Open(file)

	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		return nil, err
	}
	decoder := json.NewDecoder(bytes.NewReader(byteValue))
	return decoder, nil
}
