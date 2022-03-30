//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package mongo

import (
	"bytes"
	"os/exec"
)

// Mongo Import
// Execute a bash command
// mongoimport: allow to upload a file on a mongo db inside a specific collection
func Import(uri, collection, file string) (err error, onStdOut string, onStdErr string) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	// Specifing command: 	mongoimport (import content; JSON, CSV, TSV)
	//						uri (perform command on this mongo database)
	//						collection (perform command on this collection of the mongo database)
	//						file (the file that has to be imported)
	bashCommand := exec.Command("mongoimport", "--uri", uri, "--collection", collection, "--file", file)
	bashCommand.Stdout = &stdout // assing command I/O stdout to get exec package stdout
	bashCommand.Stderr = &stderr // assign command I/O stderr to get exec package stderr
	// Start the specified command and waits for it to complete
	err = bashCommand.Run()
	return err, stdout.String(), stderr.String()
}
