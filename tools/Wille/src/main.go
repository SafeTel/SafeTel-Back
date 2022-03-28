//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// main
//

package main

import (
	wille "PostmanDbDataImplementation/core"
	"fmt"
	"os"
)

func main() {
	argv := os.Args[1:]       // Don't keep the first arg
	wille, err := wille.New() // Generate Wille object

	if err != nil {
		fmt.Fprintln(os.Stderr, "Error: ", err)
		os.Exit(1)
	}
	// Running
	if err = wille.Run(argv); err != nil {
		fmt.Fprintln(os.Stderr, "Error: ", err)
		os.Exit(1)
	}
}
