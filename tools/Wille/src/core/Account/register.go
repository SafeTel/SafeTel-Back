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
	Error  bool   `json:"error"`
	Detail string `json:"detail"`
}

func (profile *Profile) CheckRegisterSuccess(rSuccess RegisterSuccess) error {
	if !rSuccess.Created {
		return errors.New("Register: Unexpected error ")
	}

	if rSuccess.Token == "" {
		return errors.New("Unexpected Error")
	}
	return nil
}

func (profile *Profile) Register(client *resty.Client) (string, error) {
	var rSuccess RegisterSuccess
	var rFailure RegisterError

	resp, err := client.R().
		SetBody(profile.Data).
		SetResult(&rSuccess).
		SetError(&rFailure).
		Post(profile.Config.DEV_URI_SERVER)

	if err != nil {
		return "", err
	}

	if resp.StatusCode() != 200 && rFailure.Error {
		profile.Print.Error(rFailure)
		return "", errors.New("Register - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + rFailure.Detail)
	}

	if err := profile.CheckRegisterSuccess(rSuccess); err != nil {
		return "", err
	}

	return rSuccess.Token, nil
}
