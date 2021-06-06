package dataModels

type History struct {
	Id     string `json:"id"`
	UserId string `json:"userId"`
	Values []Call `json:"history"`
}
