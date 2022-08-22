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

type LoginSuccess struct {
	Username string `json:"username"`
	Token    string `json:"token"`
}

type LoginError struct {
	Error  bool   `json:"error"`
	Detail string `json:"detail"`
}

func (profile *Profile) CheckLoginSuccess(lSuccess LoginSuccess) error {
	if lSuccess.Token == "" {
		return errors.New("Unexpected Error")
	}
	return nil
}

func (profile *Profile) Login(client *resty.Client) (string, error) {
	var lSuccess LoginSuccess
	var lFailure LoginError

	resp, err := client.R().
		SetBody(map[string]interface{}{
			"magicnumber": profile.Data.MagicNumber,
			"email":       profile.Data.Email,
			"password":    profile.Data.Password,
		}).
		SetResult(&lSuccess).
		SetError(&lFailure).
		Post(profile.Config.DEV_URI_SERVER)

	if err != nil {
		return "", err
	}

	if resp.StatusCode() != 200 {
		profile.Print.Error(lFailure)
		return "", errors.New("Login - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + lFailure.Detail)
	}

	if err := profile.CheckLoginSuccess(lSuccess); err != nil {
		return "", err
	}

	return lSuccess.Token, nil
}
