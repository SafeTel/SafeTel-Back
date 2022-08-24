//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// post history
//

package history

import (
	"errors"
	"strconv"

	"github.com/go-resty/resty/v2"
)

type PostSuccess struct {
	Calls []Call `json:"History"`
}

type PostError struct {
	Error  bool   `json:"error"`
	Detail string `json:"details"`
}

func (history *History) postHistoryHttpRequest(client *resty.Client, token string, call Call) (*resty.Response, error, PostSuccess, PostError) {
	var pSuccess PostSuccess
	var pFailure PostError

	resp, err := client.R().
		SetBody(map[string]interface{}{
			"token": token,
			"HistoryCall": map[string]interface{}{
				"number": call.Number,
				"status": call.Status,
				"time":   call.Time,
			}}).
		SetResult(&pSuccess).
		SetError(&pFailure).
		Post("http://" + history.Config.DEV_URI_SERVER + "/account/lists/history")

	return resp, err, pSuccess, pFailure
}

func (history *History) PostHistory(client *resty.Client, token string) error {
	history.Print.Info("Uploading History...")

	for _, call := range history.Data.Calls {
		history.Print.Info("History post phone number: " + call.Number + " - Status: " + call.Status)

		resp, err, _, pFailure := history.postHistoryHttpRequest(client, token, call)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			history.Print.Error(pFailure)
			return errors.New("PostBlacklist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
		history.Print.Info("Done")
	}

	return nil
}
