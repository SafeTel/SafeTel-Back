//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// Claim box
//

package box

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

func (box *Box) claimBoxHttpRequest(client *resty.Client, token, boxId string) (*resty.Response, error, PostSuccess, PostError) {
	var cBSuccess PostSuccess
	var cBFailure PostError

	resp, err := client.R().
		SetBody(map[string]interface{}{
			"token": token,
			"boxid": boxId,
		}).
		SetResult(&cBSuccess).
		SetError(&cBFailure).
		Post("http://" + box.Config.DEV_URI_SERVER + "/box/link/claim-box")
	return resp, err, cBSuccess, cBFailure
}

func (box *Box) ClaimBox(client *resty.Client, token string) error {
	box.Print.Info("Claiming Box...")

	for _, aBox := range box.Data.Boxes {

		box.Print.Info("Claiminb box with id: " + aBox.BoxId)
		resp, err, _, cBFailure := box.claimBoxHttpRequest(client, token, aBox.BoxId)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 200 && cBFailure.Error {
			box.Print.Error(cBFailure)
			return errors.New("ClaimBox - Status Code : " + strconv.Itoa(resp.StatusCode()) + "- Error: " + cBFailure.Detail)
		}
		box.Print.Info("Done")
	}
	return nil
}
