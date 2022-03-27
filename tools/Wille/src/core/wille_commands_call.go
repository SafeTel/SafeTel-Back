//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	input "PostmanDbDataImplementation/errors"
	"fmt"
)

// Print help
func (wille *Wille) printHelp() {
	fmt.Println("")
	fmt.Println("Usage:")
	fmt.Println("./wille [options] argument...")
	fmt.Println("")
	fmt.Println("Options:")
	fmt.Println("\tshow\tShow the user configuration")
	fmt.Println("\t./wille show <data>")
	fmt.Println("")
	fmt.Println("\tupload\tUpload on the database the user configuration")
	fmt.Println("\t./wille upload <data>")
	fmt.Println("")
	fmt.Println("\thash\tHash a password")
	fmt.Println("\t./wille hash <password>")
	fmt.Println("")
	fmt.Println("Arguments:")
	fmt.Println("\t<data> The name of a user defined inside the model folder")
	fmt.Println("")
	fmt.Println("\t<password> Plain text password")
	fmt.Println("")

}

// Random command
// generate randomly a new user to upload on the db
func (wille *Wille) random(name string) error {
	InfoLogger.Println(name)
	return nil
}

// Compute Input command
// options: command + parameter in input
func (wille *Wille) compute(options []string) error {
	var optionsNumber int = len(options)

	for i := 0; i < len(options); i++ {
		switch options[i] {
		case "random":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing user argument for random option flag"}
			}
			i++
			err := wille.random(options[i])
			return err
		case "show":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing model name for showing"}
			}
			i++
			err := wille.show(options[i])
			return err
		case "upload":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing model name for upload"}
			}
			i++
			err := wille.upload(options[i])
			return err
		case "hash":
			if (i + 1) >= optionsNumber {
				return &input.Error{Msg: "Missing password for hashion"}
			}
			i++
			err := wille.hash(options[i])
			return err
		case "help":
			wille.printHelp()
			return nil
		default:
			wille.printHelp()
			return &input.Error{Msg: "Unknow Input: " + options[i]}
		}
	}
	return nil
}
