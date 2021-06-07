//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - atlasClientDisconnection_test.go
//

package tests

import (
	"log"
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
)

func Test_DisconnectMongoAtlasClient_SimpleCall_NoPanic(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")

	origLogFatalf := dbCnct.LogFatal
	dbCnct.LogFatal = func(args ...interface{}) { // Override the dbCnct.LogFatal basic definition
		log.Panic(args)
	}

	// Assert
	defer func() { dbCnct.LogFatal = origLogFatalf }() // After this test, replace the original fatal function
	defer func() {                                     // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DisconnectMongoAtlasClient: Error: Got a Panic while trying to disconnect, err %s", err)
		}
	}()

	atlasClient := dbCnct.CreateConnectionToAtlas()

	// Act
	dbCnct.DisconnectMongoAtlasClient(atlasClient)
}
