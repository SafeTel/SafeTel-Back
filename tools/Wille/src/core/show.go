//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"errors"
)

type ShowJson struct {
	Infos string `json:"infos"`
	Pwd   string `json:"password"`
}

// Domain Layer - Core Functionalities

func (wille *Wille) printEmptyOrUndefinedKey(key string) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[31mEmpty or not defined\033[0m")
}

func (wille *Wille) printDefinedKeyWithValue(key string, value interface{}) {
	InfoLogger.Println(tabPrefixForJsonPrint, "-\033[36m", key, "\033[0mvalue: \033[32mdefined\033[0m Value: \033[36m", value, ResetColor)
}

// Repository Layer - Error Checking

func (wille *Wille) checkShowJsonContent(name string) error {
	s, err := wille.openAndUnmarshalJson("Data/" + name + "/Show.json")

	if err != nil {
		return err
	}
	keys := []string{
		"infos",
		"password"}

	err = wille.checkAndShowJsonContent(s, keys, nil)
	if err != nil {
		return errors.New("Problem with json file " + name + "/Show.json" + ": " + err.Error())
	}
	return nil
}

// Service Layer - Interface

func (wille *Wille) showListFolder(name string) error {
	listFolderContent, err := wille.checkListJsonFolder(name)

	if err != nil {
		return err
	}
	if listFolderContent&(0b00000001) == valid {
		InfoLogger.Println("\t- Blacklist.json: \033[32mFinded\033[0m")
		err = wille.checkAndShowBlacklistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Blacklist.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("\t- History.json: \033[32mFinded\033[0m")
		err = wille.checkAndShowHistoryJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- History.json: \033[32mMissing\033[0m")
	}
	if listFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("\t- Whitelist.json: \033[32mFinded\033[0m")
		err = wille.checkAndShowWhitelistJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("\t- Whitelist.json: \033[32mMissing\033[0m")
	}
	return nil
}

// Repository Layer

func (wille *Wille) printShowJsonFile(name string) error {
	return nil
}

func (wille *Wille) show(name string) error {
	modelFolderContent, err := wille.checkModelFolder(name)

	if err != nil {
		return err
	}
	if modelFolderContent&(0b00000001) == valid {
		InfoLogger.Println("Profile.json: \033[32mFinded\033[0m")
		err = wille.checkAndShowProfileJsonContent(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Profile.json: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000010)>>1 == valid {
		InfoLogger.Println("Lists folder: \033[32mFinded\033[0m")
		err = wille.showListFolder(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Lists folder: \033[31mMissing\033[0m")
	}
	if modelFolderContent&(0b00000100)>>2 == valid {
		InfoLogger.Println("Show.json: \033[32mFinded\033[0m")
		err = wille.checkShowJsonContent(name)
		if err != nil {
			return err
		}
		err = wille.printShowJsonFile(name)
		if err != nil {
			return err
		}
	} else {
		InfoLogger.Println("Show.json: \033[31mMissing\033[0m")
	}
	return nil
}
