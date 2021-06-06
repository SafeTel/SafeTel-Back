package dataModels

import "time"

type Call struct {
	PhoneNumber `json:"number"`
	Origin      string    `json:"origin"`
	Time        time.Time `json:"time"`
}
