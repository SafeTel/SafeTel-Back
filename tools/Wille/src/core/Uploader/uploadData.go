//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package uploader

import "errors"

func (uploader *Uploader) uploadAccount() (string, error) {
	var registerErr error
	var loginErr error
	var token string

	token, registerErr = uploader.Profile.Register(uploader.HttpClient)

	if registerErr == nil {
		return token, nil
	}

	token, loginErr = uploader.Profile.Login(uploader.HttpClient)

	if loginErr == nil {
		return token, nil
	}

	return "", errors.New("Error from Register and Login: " + registerErr.Error() + " <|||> " + loginErr.Error())
}

func (uploader *Uploader) uploadAccountLists(token string) error {
	return nil
}

func (uploader *Uploader) uploadData() error {
	token, err := uploader.uploadAccount()

	if err != nil {
		return err
	}

	err = uploader.uploadAccountLists(token)

	if err != nil {
		return err
	}

	// uploader.uploadEmbedded()

	return nil
}
