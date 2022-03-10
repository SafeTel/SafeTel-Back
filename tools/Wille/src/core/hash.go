//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

import (
	"golang.org/x/crypto/sha3"
)

func (wille *Wille) hash(password string) error {
	h := sha3.New512()

	InfoLogger.Println("You are going to hash the password: '", password, "' using SHA 3 in 512 bytes")
	InfoLogger.Println("Processing...")
	InfoLogger.Println("Hashing the password...")
	_, err := h.Write([]byte(password))

	if err != nil {
		return err
	}

	sum := h.Sum(nil)

	InfoLogger.Println("Done!")
	InfoLogger.Println("Your hashed password is:")
	InfoLogger.Printf("%x\n", sum)

	return nil
}
