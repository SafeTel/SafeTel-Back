//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - AddWhitelistCollection_test.go
//

package tests

import (
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
	whitelist "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList"
)

func Test_AddWhitelistPhoneNumberForUserId_OnePhoneNumber_ValidAddition(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("WHAT THE FUCK AddWhitelistPhoneNumberForUserId: Error: Got a Panic while trying to add one phoneNumber, err %s", err)
		}
	}()
	client := dbCnct.CreateConnectionToAtlas()
	whitelist := whitelist.NewWhilelist(client, os.Getenv("DBName"))
	var getResult models.ControlList
	var addWhitelistPhoneNumberForUserIdTest = struct { // Defining data var Delete method
		input    string // input
		expected string // expected result
	}{"0102030405", "0102030405"}

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("AddWhitelistPhoneNumberForUserId: Error: Got a Panic while trying to add one phoneNumber, err %s", err)
		}
	}()
	whitelist.AddWhitelistPhoneNumberForUserId("1", addWhitelistPhoneNumberForUserIdTest.input)
	getResult = whitelist.GetWhiteListForUserId("1")

	// Assert
	for _, elem := range getResult.Number {
		if elem == addWhitelistPhoneNumberForUserIdTest.expected {
			whitelist.DelWhiteListPhoneNumberForUserId("1", addWhitelistPhoneNumberForUserIdTest.input)
			return
		}
	}
	tester.Errorf("AddWhitelistPhoneNumberForUserId: expected %s, not founded", addWhitelistPhoneNumberForUserIdTest.expected)
}
