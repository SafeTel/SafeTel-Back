//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Call Data Model - Call.go
//

package models

import "time"

type Call struct {
	Number string    `json:"number"`
	Origin string    `json:"origin"`
	Time   time.Time `json:"time"`
}
