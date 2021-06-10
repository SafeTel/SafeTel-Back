//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - GetHistoryCollection_test.go
//

package tests

import (
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	history "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/History"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
)

func Test_GetHistoryForUserId_NoValues_FoundNotEmptyList(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	history := history.NewHistory(client, os.Getenv("DBName"))
	var getResult models.History

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("GetHistoryForUserId: Error: Got a Panic while trying to get history, err %s", err)
		}
	}()
	getResult = history.GetHistoryForUserId("1")

	// Assert
	if len(getResult.Values) == 0 {
		tester.Errorf("GetHistoryForUserId: empty result")
	}
}
