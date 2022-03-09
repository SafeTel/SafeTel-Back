//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// main
//

package main

import (
	cmd "PostmanDbDataImplementation/core"
	"fmt"
	"os"
)

func main() {
	argv := os.Args[1:] // Don't keep the first arg
	wille, err := cmd.New()

	if err != nil {
		fmt.Fprintln(os.Stderr, "Error: ", err)
	}
	err = wille.Run(argv)

	if err != nil {
		fmt.Fprintln(os.Stderr, "Error: ", err)
	}
}
