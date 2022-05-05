//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	utils "PostmanDbDataImplementation/core/Utils"
	"errors"
)

// Upload the content of Lists folder. The files that will be uploaded are:
// data/name/Lists:	Blacklist.json
//					History.json
//					Whitelist.json
func (wille *Wille) uploadListFiles(name string) error {
	content, err := utils.CheckListFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		err = wille.Blacklist.UploadBlacklistFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.History.UploadHistoryFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000100)>>2 == valid {
		err = wille.Whitelist.UploadWhitelistFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}

// Upload the content of Embedded folder. The files that will be uploaded are:
// data/name/Embedded:	Box.json
//
func (wille *Wille) uploadEmbeddedFiles(name string) error {
	content, err := utils.CheckEmbeddedFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		err = wille.Box.UploadBoxFile(name)
		if err != nil {
			return err
		}
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
	if !wille.isValidApiKey() {
		return errors.New("ApiKey not valid")
	}

	content, err := utils.CheckModelFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		err = wille.Profile.UploadProfileFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadListFiles(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00001000)>>3 == valid {
		err = wille.uploadEmbeddedFiles(name)
		if err != nil {
			return err
		}
	}
	return nil
}
