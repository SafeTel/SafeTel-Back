//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - AddBlacklistCollection_test.go
//

package tests

import (
	"os"
	"testing"

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList"
	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
)

func Test_AddBlacklistPhoneNumberForUserId_OnePhoneNumber_ValidAddition(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("WHAT THE FUCK AddBlacklistPhoneNumberForUserId: Error: Got a Panic while trying to add one phoneNumber, err %s", err)
		}
	}()
	client := dbCnct.CreateConnectionToAtlas()
	blackList := blackList.NewBlacklist(client, os.Getenv("DBName"))
	var getResult models.ControlList
	var addBlacklistPhoneNumberForUserIdTest = struct { // Defining data var Delete method
		input    string // input
		expected string // expected result
	}{"0102030405", "0102030405"}

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("AddBlacklistPhoneNumberForUserId: Error: Got a Panic while trying to add one phoneNumber, err %s", err)
		}
	}()
	blackList.AddBlacklistPhoneNumberForUserId("1", addBlacklistPhoneNumberForUserIdTest.input)
	getResult = blackList.GetBlacklistForUserId("1")

	// Assert
	for _, elem := range getResult.Number {
		if elem == addBlacklistPhoneNumberForUserIdTest.expected {
			blackList.DelBlacklistPhoneNumberForUserId("1", addBlacklistPhoneNumberForUserIdTest.input)
			return
		}
	}
	tester.Errorf("AddBlacklistPhoneNumberForUserId: expected %s, not founded", addBlacklistPhoneNumberForUserIdTest.expected)
}
