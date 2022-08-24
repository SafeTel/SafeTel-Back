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
	Detail string `json:"details"`
}

func (profile *Profile) CheckLoginSuccess(lSuccess LoginSuccess) error {
	if lSuccess.Token == "" {
		return errors.New("Unexpected Error")
	}
	return nil
}

func (profile *Profile) loginHttpRequest(client *resty.Client) (*resty.Response, error, LoginSuccess, LoginError) {
	var lSuccess LoginSuccess
	var lFailure LoginError

	profile.Print.Info("Login")
	resp, err := client.R().
		SetBody(map[string]interface{}{
			"magicnumber": profile.Data.MagicNumber,
			"email":       profile.Data.Email,
			"password":    profile.Data.Password,
		}).
		SetResult(&lSuccess).
		SetError(&lFailure).
		Post("http://" + profile.Config.DEV_URI_SERVER + "/auth/login")
	return resp, err, lSuccess, lFailure
}

func (profile *Profile) Login(client *resty.Client) (string, error) {
	profile.Print.Info("Performing a login...")

	resp, err, lSuccess, lFailure := profile.loginHttpRequest(client)

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
	profile.Print.Info("Done")
	return lSuccess.Token, nil
}
