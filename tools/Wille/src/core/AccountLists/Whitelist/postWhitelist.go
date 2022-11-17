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
	Detail string `json:"details"`
}

func (whitelist *Whitelist) postBlacklistHttpRequest(client *resty.Client, token, phoneNumber string) (*resty.Response, error, PostSuccess, PostError) {
	var pSuccess PostSuccess
	var pFailure PostError

	resp, err := client.R().
		SetBody(map[string]interface{}{
			"token":  token,
			"number": phoneNumber,
		}).
		SetResult(&pSuccess).
		SetError(&pFailure).
		Post("http://" + whitelist.Config.DEV_URI_SERVER + "/account/lists/whitelist")

	return resp, err, pSuccess, pFailure

}

func (whitelist *Whitelist) PostWhitelist(client *resty.Client, token string) error {
	whitelist.Print.Info("Uploading Whitelist...")

	for _, phoneNumber := range whitelist.Data.PhoneNumbers {

		whitelist.Print.Info("Whitelist post phone number: " + phoneNumber)
		resp, err, _, pFailure := whitelist.postBlacklistHttpRequest(client, token, phoneNumber)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			whitelist.Print.Error(pFailure)
			return errors.New("PostWhitelist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
		whitelist.Print.Info("Done")
	}
	return nil
}
