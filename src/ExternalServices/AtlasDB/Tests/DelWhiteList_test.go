//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - DelWhitelistCollection_test.go
//

package tests

import (
	"os"
	"testing"

	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
	whiteList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList"
)

func Test_DeleteWhiteListPhoneNumberForUserId_DeleteOnePhoneNumber_ValidDeletion(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	whitelist := whiteList.NewWhilelist(client, os.Getenv("DBName"))
	var getResult models.ControlList
	var getWhitelistForUserIdTest = struct { // Defining data var Delete method
		input    string      // input
		expected interface{} // expected result
	}{"0102030405", nil}
	whitelist.AddWhitelistPhoneNumberForUserId("1", getWhitelistForUserIdTest.input)

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DelWhiteListPhoneNumberForUserId: Error: Got a Panic while trying to delete one phoneNumber, err %s", err)
		}
	}()
	whitelist.DelWhiteListPhoneNumberForUserId("1", getWhitelistForUserIdTest.input)
	getResult = whitelist.GetWhiteListForUserId("1")

	// Assert
	for _, elem := range getResult.Number {
		if elem == getWhitelistForUserIdTest.input {
			tester.Errorf("DelWhiteListPhoneNumberForUserId: expected %s, Found %s", getWhitelistForUserIdTest.expected, getWhitelistForUserIdTest.input)
		}
	}
}

func Test_DeleteWhiteListPhoneNumberForUserId_UnknowPhoneNumber_DeletionError(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")
	client := dbCnct.CreateConnectionToAtlas()
	whitelist := whiteList.NewWhilelist(client, os.Getenv("DBName"))
	WhitelistNumberlen := len(whitelist.GetWhiteListForUserId("1").Number)
	var getResultNumber int
	var getWhitelistForUserIdTest = struct { // Defining data var Delete method
		input    string // input
		expected int    // expected result
	}{"DOESN'T EXIST", WhitelistNumberlen}

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DelWhiteListPhoneNumberForUserId: Error: Got a Panic while trying to delete an unknow phoneNumber, err %s", err)
		}
	}()
	whitelist.DelWhiteListPhoneNumberForUserId("1", getWhitelistForUserIdTest.input)
	getResultNumber = len(whitelist.GetWhiteListForUserId("1").Number)

	// Assert
	if getResultNumber != getWhitelistForUserIdTest.expected {
		tester.Errorf("DelWhiteListPhoneNumberForUserId: expected %d, Found %d", getWhitelistForUserIdTest.expected, getResultNumber)
	}
}
