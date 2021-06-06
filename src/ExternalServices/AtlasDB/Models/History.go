//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// History Data Model - history.go
//

package dataModels

type History struct {
	Id     string `json:"id"`
	UserId string `json:"userId"`
	Values []Call `json:"history"`
}
