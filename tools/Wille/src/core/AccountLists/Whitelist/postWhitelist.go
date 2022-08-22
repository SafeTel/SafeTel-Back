//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// post Whitelist
//

package whitelist

import (
	"errors"
	"strconv"

	"github.com/go-resty/resty/v2"
)

type PostSuccess struct {
	Whitelist []string `json:"Whitelist"`
}

type PostError struct {
	Error  bool   `json:"error"`
	Detail string `json:"detail"`
}

func (whitelist *Whitelist) PostWhitelist(client *resty.Client, token string) error {
	var pSuccess PostSuccess
	var pFailure PostError

	for _, phoneNumber := range whitelist.Data.PhoneNumbers {
		resp, err := client.R().
			SetBody(map[string]interface{}{
				"token":  token,
				"number": phoneNumber,
			}).
			SetResult(&pSuccess).
			SetError(&pFailure).
			Post(whitelist.Config.DEV_URI_SERVER)
		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			whitelist.Print.Error(pFailure)
			return errors.New("PostWhitelist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
	}
	return nil
}
