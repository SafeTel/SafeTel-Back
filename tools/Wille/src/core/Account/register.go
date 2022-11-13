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

	// Request type
	"github.com/go-resty/resty/v2"
)

type RegisterSuccess struct {
	Created  bool   `json:"created"`
	Username string `json:"username"`
	Token    string `json:"token"`
}

type RegisterError struct {
	Error  bool   `json:"error"`
	Detail string `json:"details"`
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

func (profile *Profile) registerHttpRequest(client *resty.Client) (*resty.Response, error, RegisterSuccess, RegisterError) {
	var rSuccess RegisterSuccess
	var rFailure RegisterError

	resp, err := client.R().
		SetBody(
			map[string]interface{}{
				"magicnumber": profile.Data.MagicNumber,
				"email":       profile.Data.Email,
				"username":    profile.Data.Username,
				"password":    profile.Data.Password,
				"CustomerInfos": map[string]interface{}{
					"firstName":   profile.Data.CustomerInfos.Firstname,
					"lastName":    profile.Data.CustomerInfos.Lastname,
					"phoneNumber": profile.Data.CustomerInfos.PhoneNumber,
				},
				"Localization": map[string]interface{}{
					"country": profile.Data.Localization.Country,
					"region":  profile.Data.Localization.Region,
					"address": profile.Data.Localization.Country,
				}},
		).
		SetResult(&rSuccess).
		SetError(&rFailure).
		Post("http://" + profile.Config.DEV_URI_SERVER + "/auth/register")

	return resp, err, rSuccess, rFailure
}

func (profile *Profile) Register(client *resty.Client) (string, error) {
	profile.Print.Info("Performing a register...")

	resp, err, rSuccess, rFailure := profile.registerHttpRequest(client)

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

	profile.Print.Info("Done")

	return rSuccess.Token, nil
}
