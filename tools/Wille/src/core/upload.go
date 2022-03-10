//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package cmd

// Upload the content of Lists folder. The files that will be uploaded are:
// data/name/Lists:	Blacklist.json
//					History.json
//					Whitelist.json
func (wille *Wille) uploadListFiles(name string) error {
	content, err := wille.checkListFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadBlacklistFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadHistoryFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000100)>>2 == valid {
		err = wille.uploadWhitelistFile(name)
		if err != nil {
			return err
		}
	}
	return nil
}

// Upload wille command
// upload a model to the database
// Upload the following files
// data/Name:	Profile.json
//				Lists/:	Blacklist.json
//						History.json
//						Whitelist.json
func (wille *Wille) upload(name string) error {
	content, err := wille.checkModelFolder(name)

	if content&(0b00000001) == valid {
		err = wille.uploadProfileFile(name)
		if err != nil {
			return err
		}
	}
	if content&(0b00000010)>>1 == valid {
		err = wille.uploadListFiles(name)
		if err != nil {
			return err
		}
	}
	return nil
}
