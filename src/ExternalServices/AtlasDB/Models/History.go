//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// History Data Model - History.go
//

package models

type History struct {
	UserId string `json:"userId"`
	Values []struct {
		Number string `json:"number" bson:"number"`
		Origin string `json:"origin" bson:"origin"`
		Time   string `json:"time" bson:"time"`
	} `json:"history" bson:"history"`
}
