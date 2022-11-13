//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// post blacklist
//

package blacklist

import (
	"errors"
	"strconv"

	"github.com/go-resty/resty/v2"
)

type PostSuccess struct {
	Blacklist []string `json:"Blacklist"`
}

type PostError struct {
	Error  bool   `json:"error"`
	Detail string `json:"details"`
}

func (blacklist *Blacklist) postBlacklistHttpRequest(client *resty.Client, token, phoneNumber string) (*resty.Response, error, PostSuccess, PostError) {
	var pSuccess PostSuccess
	var pFailure PostError

	resp, err := client.R().
		SetBody(map[string]interface{}{
			"token":  token,
			"number": phoneNumber,
		}).
		SetResult(&pSuccess).
		SetError(&pFailure).
		Post("http://" + blacklist.Config.DEV_URI_SERVER + "/account/lists/blacklist")

	return resp, err, pSuccess, pFailure
}

func (blacklist *Blacklist) PostBlacklist(client *resty.Client, token string) error {
	blacklist.Print.Info("Uploading Blacklist...")

	for _, phoneNumber := range blacklist.Data.PhoneNumbers {

		blacklist.Print.Info("Blacklist post phone number: " + phoneNumber)
		resp, err, _, pFailure := blacklist.postBlacklistHttpRequest(client, token, phoneNumber)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			blacklist.Print.Error(pFailure)
			return errors.New("PostBlacklist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
		blacklist.Print.Info("Done")
	}
	return nil
}
