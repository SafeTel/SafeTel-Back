//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// GetHistoryResponse
//

package responsesUserLists

import "time"

type GetHistoryResponse struct {
	Values []struct {
		Number string    `json:"number" bson:"number"`
		Origin string    `json:"origin" bson:"origin"`
		Time   time.Time `json:"time" bson:"time"`
	} `json:"history" bson:"History"`
}
