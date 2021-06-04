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

	for _, elem := range mongoDbConnectedClientTests {
		_, err := GetConnectedMongoAtlasClient(elem.input)
		testResults = append(testResults, err)
	}

	// Assert

	for index, elem := range mongoDbConnectedClientTests {
		if testResults[index] != elem.expected {
			tester.Errorf("GetConnectedMongoAtlasClient: expected %s, got %s", elem.expected, testResults[index])
		}
	}

}
