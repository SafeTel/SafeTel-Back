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
	err := uploader.Blacklist.PostBlacklist(uploader.HttpClient, token)

	if err != nil {
		uploader.Print.Info("Post Blacklist Error: " + err.Error())
	}
	err = uploader.Whitelist.PostWhitelist(uploader.HttpClient, token)

	if err != nil {
		uploader.Print.Info("Post Whitelist Error: " + err.Error())
		// return err
	}
	err = uploader.History.PostHistory(uploader.HttpClient, token)

	if err != nil {
		uploader.Print.Info("Post History Error: " + err.Error())
		// return err
	}

	return nil
}

func (uploader *Uploader) uploadEmbedded(token string, name string) error {
	err := uploader.Box.InsertBoxes(name)

	if err != nil {
		return err
	}

	err = uploader.Box.ClaimBox(uploader.HttpClient, token)

	if err != nil {
		return err
	}

	return nil
}

func (uploader *Uploader) uploadData(name string) error {
	token, err := uploader.uploadAccount()

	if err != nil {
		return err
	}

	uploader.Print.Info(token)

	err = uploader.uploadAccountLists(token)

	if err != nil {
		return err
	}

	err = uploader.uploadEmbedded(token, name)

	if err != nil {
		return err
	}

	return nil
}

func (uploader *Uploader) UploadBoxesFromFile(filePath string) error {
	if err := uploader.Box.LoadFile(filePath); err != nil {
		return err
	}

	err := uploader.Box.InsertBoxes(filePath)

	if err != nil {
		return err
	}
	return nil
}
