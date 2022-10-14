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

	if err := wille.Uploader.LoadModel(name); err != nil {
		return err
	}

	wille.Print.Info("Showing Content:	")

	wille.Uploader.Profile.ShowProfile()
	wille.Uploader.Blacklist.ShowBlacklist()
	wille.Uploader.Whitelist.ShowWhitelist()
	wille.Uploader.History.ShowHistory()
	wille.Uploader.Box.ShowBox()

	return nil
}
