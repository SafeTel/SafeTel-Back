//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - GelBlacklistCollection_test.go
//

package tests

import (
	"os"
	"testing"

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList"
	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
)

func Test_GetBlacklistForUserId_NoValues_FoundNotEmptyList(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	blackList := blackList.NewBlacklist(client, os.Getenv("DBName"))
	var getResult models.ControlList

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("GetBlacklistForUserId: Error: Got a Panic while trying to get blacklist, err %s", err)
		}
	}()
	getResult = blackList.GetBlacklistForUserId("1")

	// Assert
	if len(getResult.Number) == 0 {
		tester.Errorf("GetBlacklistForUserId: empty result")
	}
}
