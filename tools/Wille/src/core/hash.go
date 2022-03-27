//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	"golang.org/x/crypto/sha3"
)

// Hash Wille command
// Hash using sha3 in 512 bytes the input
func (wille *Wille) hash(password string) error {
	hasher := sha3.New512()
	_, err := hasher.Write([]byte(password))

	if err != nil {
		return err
	}
	sum := hasher.Sum(nil)

	InfoLogger.Printf("Your hashed password is: %x\n", sum)

	return nil
}
