//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// inputErrors
//

package error

import "fmt"

type Error struct {
	Msg string
}

func (e *Error) Error() string {
	return fmt.Sprintf("Input error: %v", e.Msg)
}

func throwError() error {
	return &Error{Msg: "False cmd as input"}
}
