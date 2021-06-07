//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - DelHistoryCollection_test.go
//

package tests

import (
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	history "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/History"
)

type CallTest struct {
	UserId    string
	Number    string
	timeStamp int
}

func Test_DelHistoryForUserId_DeleteOneCall_FoundNotEmptyList(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	history := history.NewHistory(client, os.Getenv("DBName"))
	HistoryCallLen := len(history.GetHistoryForUserId("1"))
	var getResultNumber int
	var delHistoryForUserIdTest = struct { // Defining data var Delete method
		input    CallTest
		expected int // expected result
	}{CallTest{UserId: "1", Number: "DOESN'T EXIST", timeStamp: 0}, HistoryCallLen}

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("GetHistoryForUserId: Error: Got a Panic while trying to get history, err %s", err)
		}
	}()
	history.DelHistoryCallForUserId(delHistoryForUserIdTest.input.UserId, delHistoryForUserIdTest.input.Number, delHistoryForUserIdTest.input.timeStamp)
	getResultNumber = len(history.GetHistoryForUserId("1"))

	// Assert
	if getResultNumber != delHistoryForUserIdTest.expected {
		tester.Errorf("DelHistoryCallForUserId: expected %d, Found %d", delHistoryForUserIdTest.expected, getResultNumber)
	}
}
