//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// WhiteList Data Models - WhiteList.go
//

package models

type WhiteListDataFormat struct {
	UserId       string   `json:"userId"`
	PhoneNumbers []string `json:"phoneNumbers"`
}
