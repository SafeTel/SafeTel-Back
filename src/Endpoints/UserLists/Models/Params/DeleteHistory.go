//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// DeleteHistory
//

package paramsUserLists

type DeleteHistory struct {
	UserId string `json:"userId"`
	Number string `json:"number"`
	Time   int    `json:"time"`
}
