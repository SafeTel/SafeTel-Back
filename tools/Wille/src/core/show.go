//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	utils "PostmanDbDataImplementation/core/Utils" // Check folders and reading methods
	"errors"                                       // Generate new errors
)

type Show struct {
	Infos    string `json:"infos"`
	Password string `json:"password"`
}

// Check the content of a Show object
func (wille *Wille) checkShowObjectDataValidity(name string, show Show) error {
	if show.Infos == "" {
		return errors.New("Problem with json file " + name + "/Show.jsonBox Missing Show Infos value")
	}
	if show.Password == "" {
		return errors.New("Problem with json file " + name + "/Show.jsonBox Missing Show Password value")
	}
	return nil
}

// Check the content of the Show.json file and check if the data has not been uploaded yet
func (wille *Wille) checkShowDataValidity(name string) (Show, error) {
	var show Show

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Show.json")
	if err != nil {
		return Show{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&show); err != nil {
		return Show{}, err
	}
	// check Json Content
	if err = wille.checkShowObjectDataValidity(name, show); err != nil {
		return Show{}, err
	}

	return show, nil
}

func (wille *Wille) showShow(show Show) {
	wille.Print.DefinedKeyWithValueWithTab("Infos", show.Infos)
	wille.Print.DefinedKeyWithValueWithTab("Password", show.Password)
}

// Check the content of the Show.json file and print it
func (wille *Wille) checkAndShowShowJsonContent(name string) error {
	show, err := wille.checkShowDataValidity(name)
	if err != nil {
		return err
	}

	wille.showShow(show)
	return nil
}

// Check the content of the Lists folder and print it
func (wille *Wille) showListFolder(name string) error {
	listFolderContent, err := utils.CheckListFolder(name)
	var valid byte = 1

	if err != nil {
		return err
	}
	if listFolderContent&(0b00000001) == valid {
		wille.Print.Info("\t- Blacklist.json: \033[32mFinded\033[0m")
		// Check the content of the Blacklist.json file and print the elements
		err = wille.Blacklist.CheckAndShowBlacklistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("\t- Blacklist.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000010)>>1 == valid {
		wille.Print.Info("\t- History.json: \033[32mFinded\033[0m")
		// Check the content of the History.json file and print the elements
		err = wille.History.CheckAndShowHistoryJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("\t- History.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000100)>>2 == valid {
		wille.Print.Info("\t- Whitelist.json: \033[32mFinded\033[0m")
		// Check the content of the Whitelist.json file and print the elements
		err = wille.Whitelist.CheckAndShowWhitelistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("\t- Whitelist.json: \033[32mMissing\033[0m")
	}
	return nil
}

func (wille *Wille) showEmbeddedFolder(name string) error {
	listFolderContent, err := utils.CheckEmbeddedFolder(name)
	var valid byte = 1

	if err != nil {
		return err
	}
	if listFolderContent&(0b00000001) == valid {
		wille.Print.Info("\t- Box.json: \033[32mFinded\033[0m")
		// Check the content of the Box.json file and print the elements
		err = wille.Box.CheckAndShowBoxJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("\t- Blacklist.json: \033[32mMissing\033[0m")
	}
	return nil
}

// Show wille command
// Check the content of a model folder
// Print the content of the following files
// data/Name:	Profile.json
//				Show.json
//				Lists/:	Blacklist.json
//						History.json
//						Whitelist.json
// The right content is printed in Green
// The missing content is printed in Red
// The unknown content is printed in Yellow
func (wille *Wille) show(name string) error {
	modelFolderContent, err := utils.CheckModelFolder(name) // Return, stored inside a bit, the available files and folders of the model(name) folder
	var valid byte = 1

	if err != nil {
		return err
	}
	if modelFolderContent&(0b00000001) == valid {
		wille.Print.Info("Profile.json: \033[32mFinded\033[0m")
		// Check the content of the Profile.json file and print the elements
		err = wille.Profile.CheckAndShowProfileJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("Profile.json: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Profile.json file")
	}
	if modelFolderContent&(0b00000010)>>1 == valid {
		wille.Print.Info("Lists folder: \033[32mFinded\033[0m")
		// Check the content of the Lists folder and print the elements
		err = wille.showListFolder(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("Lists folder: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Lists folder")
	}
	if modelFolderContent&(0b00000100)>>2 == valid {
		wille.Print.Info("Show.json: \033[32mFinded\033[0m")
		// Check the content of the Show.json file and print the elements
		err = wille.checkAndShowShowJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("Show.json: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Show.json file")
	}
	if modelFolderContent&(0b00001000)>>3 == valid {
		wille.Print.Info("Embedded folder: \033[32mFinded\033[0m")
		// Check the content of the Embedded folder and print the elements
		err = wille.showEmbeddedFolder(name)
		if err != nil {
			return err
		}
	} else {
		wille.Print.Info("Embedded folder: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Embedded folder")
	}

	return nil
}
