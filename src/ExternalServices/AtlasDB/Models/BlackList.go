//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// BlackList Data Models - BlackList.go
//

package models

type BlackListDataFormat struct {
	UserId       string   `json:"userId"`
	PhoneNumbers []string `json:"phoneNumbers"`
}
