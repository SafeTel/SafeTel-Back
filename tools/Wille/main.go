//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// main
//

package main

import (
	cmd "PostmanDbDataImplementation/cmd/WILLE"
	"log"
	"os"
)

func configureLogs() {
	log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds | log.Lshortfile)
}

func main() {

	log.Println("Starting WILLE")

	argv := os.Args[1:] // Don't keep the first arg
	configureLogs()
	wille, err := cmd.New()

	if err != nil {
		log.Println(err)
	}
	err = wille.Run(argv)

	if err != nil {
		log.Println(err)
	}

}
