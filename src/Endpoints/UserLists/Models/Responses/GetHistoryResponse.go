//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// GetHistoryResponse
//

package responsesUserLists

type GetHistoryResponse struct {
	Values []struct {
		Number string `json:"number"`
		Origin string `json:"origin"`
		Time   string `json:"time"`
	} `json:"history"`
}
