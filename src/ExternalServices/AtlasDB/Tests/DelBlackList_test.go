//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - DelBlacklistCollection_test.go
//

package tests

import (
	"os"
	"testing"

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList"
	dbCnct "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"
	models "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Models"
)

func Test_DeleteBlacklistPhoneNumberForUserId_DeleteOnePhoneNumber_ValidDeletion(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")

	client := dbCnct.CreateConnectionToAtlas()
	blackList := blackList.NewBlacklist(client, os.Getenv("DBName"))
	var getResult models.ControlList
	var getBlacklistForUserIdTest = struct { // Defining data var Delete method
		input    string      // input
		expected interface{} // expected result
	}{"0102030405", nil}
	blackList.AddBlacklistPhoneNumberForUserId("1", getBlacklistForUserIdTest.input)

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DeleteBlacklistPhoneNumberForUserId: Error: Got a Panic while trying to delete one phoneNumber, err %s", err)
		}
	}()
	blackList.DelBlacklistPhoneNumberForUserId("1", getBlacklistForUserIdTest.input)
	getResult = blackList.GetBlacklistForUserId("1")

	// Assert
	for _, elem := range getResult.Number {
		if elem == getBlacklistForUserIdTest.input {
			tester.Errorf("DeleteBlacklistPhoneNumberForUserId: expected %s, Found %s", getBlacklistForUserIdTest.expected, getBlacklistForUserIdTest.input)
		}
	}
}

func Test_DeleteBlacklistPhoneNumberForUserId_UnknowPhoneNumber_DeletionError(tester *testing.T) {
	// Arrange
	os.Setenv("MongoAtlasClusterURI", "mongodb+srv://SafeTelBackEndUser:aSEFTHUKOM1!@safetel-back-cluster.klq5k.mongodb.net/Melchior?retryWrites=true&w=majority")
	os.Setenv("DBName", "Melchior")
	client := dbCnct.CreateConnectionToAtlas()
	blackList := blackList.NewBlacklist(client, os.Getenv("DBName"))
	blacklistNumberlen := len(blackList.GetBlacklistForUserId("1").Number)
	var getResultNumber int
	var getBlacklistForUserIdTest = struct { // Defining data var Delete method
		input    string // input
		expected int    // expected result
	}{"DOESN'T EXIST", blacklistNumberlen}

	// Act
	defer func() { // Handling a Panic
		if err := recover(); err != nil { // Recover intercept a panic
			tester.Errorf("DeleteBlacklistPhoneNumberForUserId: Error: Got a Panic while trying to delete an unknow phoneNumber, err %s", err)
		}
	}()
	blackList.DelBlacklistPhoneNumberForUserId("1", getBlacklistForUserIdTest.input)
	getResultNumber = len(blackList.GetBlacklistForUserId("1").Number)

	// Assert
	if getResultNumber != getBlacklistForUserIdTest.expected {
		tester.Errorf("DeleteBlacklistPhoneNumberForUserId: expected %d, Found %d", getBlacklistForUserIdTest.expected, getResultNumber)
	}
}
