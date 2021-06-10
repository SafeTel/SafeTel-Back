//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - atlasClientConnection_test.go
//

package tests

import (
	"log"
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
)

func Test_GetConnectedMongoAtlasClient_SimpleCall_NoPanic(tester *testing.T) {
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
			tester.Errorf("GetConnectedMongoAtlasClient: Error: Got a Panic while trying to connect, err %s", err)
		}
	}()

	// Act
	dbCnct.CreateConnectionToAtlas() // Get err from the method
}

func Test_GetConnectedMongoAtlasClient_EmptyMongoAtlasURI_Panic(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "")

	origLogFatalf := dbCnct.LogFatal
	dbCnct.LogFatal = func(args ...interface{}) { // Override the dbCnct.LogFatal basic definition
		log.Panic(args)
	}

	// Assert
	defer func() { dbCnct.LogFatal = origLogFatalf }() // After this test, replace the original fatal function
	defer func() {                                     // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			return
		}
		tester.Errorf("GetConnectedMongoAtlasClient: Error: Haven't got a panic while trying to connect with empty URI")
	}()

	// Act
	dbCnct.CreateConnectionToAtlas() // Get err from the method
}
