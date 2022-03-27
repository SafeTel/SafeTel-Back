//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import "errors"

type Show struct {
	Infos    string `json:"infos"`
	Password string `json:"password"`
}

// Check the content of a Show object
func (wille *Wille) checkShowObjectDataValidity(name string, show Show) error {
	if show.Infos == "" {
		return errors.New("Problem with json file " + name + "/Show.json" + ": Missing Show Infos value")
	}
	if show.Password == "" {
		return errors.New("Problem with json file " + name + "/Show.json" + ": Missing Show Password value")
	}
	return nil
}

// Check the content of the Show.json file and check if the data has not been uploaded yet
func (wille *Wille) checkShowDataValidity(name string) (Show, error) {
	var show Show

	decoder, err := OpenAndGenerateJsonDecoder("data/" + name + "/Show.json")
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
	wille.printDefinedKeyWithValue("Infos", show.Infos)
	wille.printDefinedKeyWithValue("Password", show.Password)
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
	listFolderContent, err := wille.checkListFolder(name)

	if err != nil {
		return err
	}
	if listFolderContent&(0b00000001) == valid {
		InfoLogger.Println("\t- Blacklist.json: \033[32mFinded\033[0m")
		// Check the content of the Blacklist.json file and print the elements
		err = wille.checkAndShowBlacklistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Blacklist.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("\t- History.json: \033[32mFinded\033[0m")
		// Check the content of the History.json file and print the elements
		err = wille.checkAndShowHistoryJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- History.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("\t- Whitelist.json: \033[32mFinded\033[0m")
		// Check the content of the Whitelist.json file and print the elements
		err = wille.checkAndShowWhitelistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Whitelist.json: \033[32mMissing\033[0m")
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
	modelFolderContent, err := wille.checkModelFolder(name) // Return, stored inside a bit, the available files and folders of the model(name) folder

	if err != nil {
		return err
	}
	if modelFolderContent&(0b00000001) == valid {
		InfoLogger.Println("Profile.json: \033[32mFinded\033[0m")
		// Check the content of the Profile.json file and print the elements
		err = wille.checkAndShowProfileJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Profile.json: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("Lists folder: \033[32mFinded\033[0m")
		// Check the content of the Lists folder and print the elements
		err = wille.showListFolder(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Lists folder: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("Show.json: \033[32mFinded\033[0m")
		// Check the content of the Show.json file and print the elements
		err = wille.checkAndShowShowJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Show.json: \033[31mMissing\033[0m")
	}
	return nil
}
