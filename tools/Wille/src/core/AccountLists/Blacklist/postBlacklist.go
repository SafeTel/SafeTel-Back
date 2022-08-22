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
	Detail string `json:"detail"`
}

func (blacklist *Blacklist) PostBlacklist(client *resty.Client, token string) error {
	var pSuccess PostSuccess
	var pFailure PostError

	for _, phoneNumber := range blacklist.Data.PhoneNumbers {
		resp, err := client.R().
			SetBody(map[string]interface{}{
				"token":  token,
				"number": phoneNumber,
			}).
			SetResult(&pSuccess).
			SetError(&pFailure).
			Post(blacklist.Config.DEV_URI_SERVER)
		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			blacklist.Print.Error(pFailure)
			return errors.New("PostBlacklist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
	}
	return nil
}
