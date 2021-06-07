//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - GelWhiteListCollection_test.go
//

package tests

import (
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
	whitelist "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList"
)

func Test_GetwhitelistForUserId_NoValues_FoundNotEmptyList(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	whitelist := whitelist.NewWhilelist(client, os.Getenv("DBName"))
	var getResult models.ControlList

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("GetWhiteListForUserId: Error: Got a Panic while trying to get whitelist, err %s", err)
		}
	}()
	getResult = whitelist.GetWhiteListForUserId("1")

	// Assert
	if len(getResult.Number) == 0 {
		tester.Errorf("GetWhiteListForUserId: empty result")
	}
}
