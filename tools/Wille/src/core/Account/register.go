//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// register
//

package profile

import (
	"errors"
	// Itoa Function
	"strconv"

	"github.com/go-resty/resty/v2"
)

type RegisterSuccess struct {
	Created  bool   `json:"created"`
	Username string `json:"username"`
	Token    string `json:"token"`
}

type RegisterError struct {
	Detail string `json:"detail"`
}

func (profile *Profile) Register(client *resty.Client) (string, error) {
	var success RegisterSuccess
	var failure RegisterError

	resp, err := client.R().
		SetBody(profile.Data).
		SetResult(&success). // or SetResult(AuthSuccess{}).
		SetError(&failure).  // or SetError(AuthError{}).
		Post(profile.Config.DEV_URI_SERVER)

	if err != nil {
		return "", err
	}

	if resp.StatusCode() != 200 {
		profile.Print.Error(failure)
		return "", errors.New("Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + failure.Detail)
	}

	return "", nil
}
