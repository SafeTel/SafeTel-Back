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
	Detail string `json:"detail"`
}

func (history *History) PostHistory(client *resty.Client, token string) error {
	var pSuccess PostSuccess
	var pFailure PostError

	for _, call := range history.Data.Calls {
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
			Post(history.Config.DEV_URI_SERVER)
		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && pFailure.Error {
			history.Print.Error(pFailure)
			return errors.New("PostBlacklist - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + pFailure.Detail)
		}
	}

	return nil
}
