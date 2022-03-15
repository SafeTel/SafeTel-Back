//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

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
		err = wille.JsonReader.checkShowJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Show.json: \033[31mMissing\033[0m")
	}
	return nil
}
