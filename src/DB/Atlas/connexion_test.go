//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// MongoDB-Atlas - connexion_test.go
//

package mongoDBAtlas

import (
	"testing"
)

func TestMongoAtlasConnexionValidatedValues(tester *testing.T) {
	// Arrange

	var mongoDbConnectedClientTests = []struct { // Defining data var Add method
		input    bool  // input
		expected error // expected result
	}{
		{false, nil},
	}

	testResults := []error{} // Data structure to keep result of tests

	// Act

	for _, elem := range mongoDbConnectedClientTests { // For each test, process
		_, err := GetConnectedMongoAtlasClient(elem.input) // Get err from the method
		testResults = append(testResults, err)             // Adding it to the testResults data structure
	}

	// Assert

	for index, elem := range mongoDbConnectedClientTests { // For each test, process
		if testResults[index] != elem.expected { // Check if error between expected and result
			tester.Errorf("GetConnectedMongoAtlasClient: expected %s, got %s", elem.expected, testResults[index]) // Raise an error
		}
	}

}
