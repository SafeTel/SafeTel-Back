//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// GetHistoryResponse
//

package responsesUserLists

type GetHistoryResponse struct {
	Values []struct {
		Number string `json:"number" bson:"number"`
		Origin string `json:"origin" bson:"origin"`
		Time   string `json:"time" bson:"time"`
	} `json:"History" bson:"history"`
}
