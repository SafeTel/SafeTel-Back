//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// GetGreyListResponse
//

package responsesUserLists

type GetGreyListResponse struct {
	BlackList []string `json:"BlackList"`
	Whitelist []string `json:"WhiteList"`
}
