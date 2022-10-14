//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"errors" // Generate new errors
)

// UploadBoxes wille command
// Get from a file its content and upload it on the database
func (wille *Wille) uploadBoxes(filePath string) error {

	var err error = nil

	if !wille.isValidApiKey() {
		return errors.New("ApiKey not valid")
	}

	err = wille.Uploader.UploadBoxesFromFile(filePath)

	if err != nil {
		return err
	}
	return nil
}

// Upload wille command
// upload a model to the database
// Upload the following files
// data/Name:	Profile.json
//				Lists/:	Blacklist.json
//						History.json
//						Whitelist.json
//				Embedded/: Box.json
func (wille *Wille) upload(name string) error {

	var err error = nil

	if !wille.isValidApiKey() {
		return errors.New("ApiKey not valid")
	}

	err = wille.Uploader.Upload(name)

	if err != nil {
		return err
	}
	return nil
}
