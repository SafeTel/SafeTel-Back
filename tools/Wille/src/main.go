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
	"log"
	"os"

	"github.com/joho/godotenv"
)

// init() is invoked before main()
// Loading variables before main() runs
func init() {
	// loads values from .env into the system
	if err := godotenv.Load("src/.env"); err != nil {
		log.Print(".env file not found")
	}
}

func main() {
	argv := os.Args[1:]          // Don't keep the first arg
	wille, err := cmd.NewWille() // Generate Wille object

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
