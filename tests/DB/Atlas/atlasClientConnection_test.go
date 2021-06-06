//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - connexion_test.go
//

package mongoDBAtlasClient_test

import (
	"os"
	"testing"

	db "github.com/SafeTel/SafeTel-Back.git/src/DB/Atlas"
)

func Test_GetConnectedMongoAtlasClient_SimpleCall_NoPanic(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("CreateConnectionToAtlas: Error: Got a Panic while trying to connect, err %s", err)
		}
	}()
	// Act
	db.CreateConnectionToAtlas() // Get err from the method
	// Assert
}

func Test_GetConnectedMongoAtlasClient_EmptyMongoAtlasURI_Panic(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "")
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			return
		}
		tester.Errorf("CreateConnectionToAtlas: Error: Haven't got a panic while trying to connect with empty URI")
	}()
	// Act
	db.CreateConnectionToAtlas() // Get err from the method
	// Assert
}
