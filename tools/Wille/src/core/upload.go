//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	input "PostmanDbDataImplementation/errors"
	"io/ioutil"
)

// Domain Layer - Core Functionalities

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

func (wille *Wille) checkModelFolder(name string) (byte, error) {
	content := byte(0b00000000)
	listOfFolderContent, err := ioutil.ReadDir("data/" + name)

	if err != nil {
		return 0, &input.Error{Msg: "Unable to open folder for name: " + name + ". Not Found: data/" + name}
	}

	for _, anElem := range listOfFolderContent {
		if anElem.Name() == "Profile.json" {
			content ^= byte(0b00000001)
		} else if anElem.Name() == "Lists" {
			content ^= byte(0b00000010)
		} else if anElem.Name() == "Show.json" {
			content ^= byte(0b00000100)
		} else {
			InfoLogger.Println("Unknow Content: \033[33m", anElem.Name(), "\033[0m")
		}
	}
	return content, nil
}

// Repository Layer

func (wille *Wille) uploadListFile(name string) error {
	content, err := wille.checkListJsonFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadBlacklistFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadHistoryFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000100)>>2 == valid {
		err = wille.uploadWhitelistFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}

func (wille *Wille) upload(name string) error {
	content, err := wille.checkModelFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadProfileFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadListFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}
