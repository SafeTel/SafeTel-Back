//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	input "PostmanDbDataImplementation/errors"
	"bufio"
	"fmt"
	"log"
	"os"
)

// Print help
func (wille *Wille) printHelp() {
	file, err := os.Open("src/help.txt")

	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
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
