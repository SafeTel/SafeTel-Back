//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Call Data Model - call.go
//

package dataModels

import "time"

type Call struct {
	PhoneNumber `json:"number"`
	Origin      string    `json:"origin"`
	Time        time.Time `json:"time"`
}
