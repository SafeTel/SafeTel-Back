//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"bytes"
	"context"
	"encoding/json"
	"io/ioutil"
	"os"
	// "go.mongodb.org/mongo-driver/mongo/readpref"
	// "go.mongodb.org/mongo-driver/bson/primitive"
)

type JsonReader struct {
	ctx context.Context
}

func (jsonReader *JsonReader) openAndGenerateJsonDecoder(file string) (*json.Decoder, error) {
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

func NewJsonReader() (*JsonReader, error) {
	jsonReader := JsonReader{ctx: context.TODO()}
	return &jsonReader, nil
}
