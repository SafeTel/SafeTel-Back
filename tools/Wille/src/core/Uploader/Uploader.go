//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package uploader

import (
	// Profile data structure
	profile "PostmanDbDataImplementation/core/Account"
	// Blacklist data structure
	blacklist "PostmanDbDataImplementation/core/AccountLists/Blacklist"
	// History data structure
	history "PostmanDbDataImplementation/core/AccountLists/History"
	// Whitelist data structure
	whitelist "PostmanDbDataImplementation/core/AccountLists/Whitelist"
	// Embedded data structure
	box "PostmanDbDataImplementation/core/Embedded"
	// Utils for config.json file
	utils "PostmanDbDataImplementation/core/Utils"
	// Print data structure
	print "PostmanDbDataImplementation/core/Utils/Print"

	// Errors data type
	"errors"
	// Clients data type
	"go.mongodb.org/mongo-driver/mongo"
)

type Uploader struct {
	Client *mongo.Client
	Print  *print.Print
	// Class for data sructures
	Blacklist *blacklist.Blacklist
	Whitelist *whitelist.Whitelist
	History   *history.History
	Profile   *profile.Profile
	Box       *box.Box
	Config    *utils.Config
}

// Upload the content of Lists folder. The files that will be uploaded are:
// data/name/Lists:	Blacklist.json
//					History.json
//					Whitelist.json
func (uploader *Uploader) uploadListFiles(name string) error {
	content, err := utils.CheckListFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		uploader.Print.Info("\t- Blacklist.json: \033[32mFinded\033[0m")
		err = uploader.Blacklist.LoadData(name)
		if err != nil {
			return err
		}
		// uploader.Print.Info(uploader.Blacklist.Data)
	} else {
		uploader.Print.Info("\t- Blacklist.json: \033[32mMissing\033[0m")
		return errors.New("Missing " + name + "/List/Blacklist.json file")
	}
	if content&(0b00000010)>>1 == valid {
		uploader.Print.Info("\t- History.json: \033[32mFinded\033[0m")
		err = uploader.History.LoadData(name)
		if err != nil {
			return err
		}
		// uploader.Print.Info(uploader.History.Data)
	} else {
		uploader.Print.Info("\t- History.json: \033[32mMissing\033[0m")
		return errors.New("Missing " + name + "/List/History.json file")
	}
	if content&(0b00000100)>>2 == valid {
		uploader.Print.Info("\t- Whitelist.json: \033[32mFinded\033[0m")
		err = uploader.Whitelist.LoadData(name)
		if err != nil {
			return err
		}
		// uploader.Print.Info(uploader.Whitelist.Data)
	} else {
		uploader.Print.Info("\t- Whitelist.json: \033[32mMissing\033[0m")
		return errors.New("Missing " + name + "/List/Whitelist.json file")
	}
	return nil
}

// Upload the content of Embedded folder. The files that will be uploaded are:
// data/name/Embedded:	Box.json
//
func (uploader *Uploader) uploadEmbeddedFiles(name string) error {
	content, err := utils.CheckEmbeddedFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		uploader.Print.Info("\t- Box.json: \033[32mFinded\033[0m")
		err = uploader.Box.LoadData(name)
		if err != nil {
			return err
		}
		// uploader.Print.Info(uploader.Box.Data)
	} else {
		uploader.Print.Info("\t- Box.json: \033[32mMissing\033[0m")
		return errors.New("Missing " + name + "/Embedded/Box.json file")
	}
	return nil
}

func (uploader *Uploader) LoadModel(name string) error {
	content, err := utils.CheckModelFolder(name)
	var valid byte = 1

	if content&(0b00000001) == valid {
		uploader.Print.Info("Profile.json: \033[32mFinded\033[0m")
		err = uploader.Profile.LoadData(name)
		if err != nil {
			return err
		}
		// uploader.Print.Info(uploader.Profile.Data)
	} else {
		uploader.Print.Info("Profile.json: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Profile.json file")
	}
	if content&(0b00000010)>>1 == valid {
		uploader.Print.Info("Lists folder: \033[32mFinded\033[0m")
		err = uploader.uploadListFiles(name)
		if err != nil {
			return err
		}
	} else {
		uploader.Print.Info("Lists folder: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Lists folder")
	}
	if content&(0b00001000)>>3 == valid {
		uploader.Print.Info("Embedded folder: \033[32mFinded\033[0m")
		err = uploader.uploadEmbeddedFiles(name)
		if err != nil {
			return err
		}
	} else {
		uploader.Print.Info("Embedded folder: \033[31mMissing\033[0m")
		return errors.New("Missing " + name + "/Embedded folder")
	}
	return nil
}

func (uploader *Uploader) uploadModels(name string) error {
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
func (uploader *Uploader) Upload(name string) error {

	if err := uploader.LoadModel(name); err != nil {
		return err
	}

	return nil
}

func New(client *mongo.Client, print *print.Print, config *utils.Config) (*Uploader, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	uploader := Uploader{Client: client}
	uploader.Print = print
	uploader.Config = config

	var err error = nil

	uploader.Blacklist, err = blacklist.New(client, print)

	if err != nil {
		return nil, err
	}
	uploader.Whitelist, err = whitelist.New(client, print)

	if err != nil {
		return nil, err
	}
	uploader.History, err = history.New(client, print)

	if err != nil {
		return nil, err
	}
	uploader.Profile, err = profile.New(client, print)

	if err != nil {
		return nil, err
	}
	uploader.Box, err = box.New(client, print, config)

	if err != nil {
		return nil, err
	}
	return &uploader, nil
}
