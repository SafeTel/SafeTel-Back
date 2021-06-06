//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - atlasClientDisconnection_test.go
//

package mongoDBAtlasClient_test

import (
	"os"
	"testing"

	db "github.com/SafeTel/SafeTel-Back.git/src/DB/Atlas"
)

func Test_DisconnectMongoAtlasClient_SimpleCall_NoPanic(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")

	// Assert
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DisconnectMongoAtlasClient: Error: Got a Panic while trying to disconnect, err %s", err)
		}
	}()

	atlasClient := db.CreateConnectionToAtlas()

	// Act
	db.DisconnectMongoAtlasClient(atlasClient)
}
