//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

import (
	input "PostmanDbDataImplementation/errors"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
)

type CustomerInfos struct {
	Firstname   string `json:"firstName"`
	Lastname    string `json:"lastName"`
	PhoneNumber string `json:"phoneNumber"`
}

type Localization struct {
	Country string `json:"country"`
	Region  string `json:"region"`
	Address string `json:"address"`
}

type Profile struct {
	Email         string        `json:"email"`
	Username      string        `json:"userName"`
	Password      string        `json:"password"`
	CustomerInfos CustomerInfos `json:"customerInfos"`
	Localization  Localization  `json:"localization"`
	Guid          string        `json:"guid"`
	Role          string        `json:"role"`
}

// Check the content of a Profile object
func (wille *Wille) checkProfileObjectDataValidity(name string, profile Profile) error {

	if profile.Email == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Email value")
	}
	if profile.Username == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Username value")
	}
	if profile.Password == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Password value")
	}
	emptyCustomerInfos := CustomerInfos{}

	if profile.CustomerInfos == emptyCustomerInfos {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile CustomerInfos value")
	}
	if profile.CustomerInfos.Firstname == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile CustomerInfos.Firstname value")
	}
	if profile.CustomerInfos.Lastname == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile CustomerInfos.Lastname value")
	}
	if profile.CustomerInfos.PhoneNumber == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile CustomerInfos.PhoneNumber value")
	}
	emptyLocalization := Localization{}

	if profile.Localization == emptyLocalization {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Localization value")
	}
	if profile.Localization.Country == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Localization.Country value")
	}
	if profile.Localization.Region == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Localization.Region value")
	}
	if profile.Localization.Address == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Localization.Address value")
	}
	if profile.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Guid value")
	}
	if profile.Role == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.json" + ": Missing Profile Role value")
	}
	return nil
}

// Check the content of the Profile.json file and check if the data has not been uploaded yet
func (wille *Wille) checkProfileDataValidity(name string) (Profile, error) {
	var profile Profile

	decoder, err := wille.JsonReader.openAndGenerateJsonDecoder("data/" + name + "/Profile.json")
	if err != nil {
		return Profile{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&profile); err != nil {
		return Profile{}, err
	}
	// check Json Content
	if err = wille.checkProfileObjectDataValidity(name, profile); err != nil {
		return Profile{}, err
	}
	return profile, nil
}

// Upload the Profile.json file
func (wille *Wille) uploadProfileFile(name string) error {
	profile, err := wille.checkProfileDataValidity(name)

	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"email": profile.Email, "guid": profile.Guid}
	if err = wille.checkDataValidityOnStorage(wille.User, filter); err != nil {
		return err
	}
	// Upload
	err, inOut, inErr := wille.mongoImport(DEV_URI_USERS_DB, "User", "data/"+name+"/Profile.json")

	if err != nil {
		return &input.Error{Msg: err.Error()}
	}
	InfoLogger.Println("StdOut: Uploading the profile file of ", name, ": ", inOut)
	InfoLogger.Println("StdErr: Uploading the profile file of ", name, ": ", inErr)
	return nil
}

func (wille *Wille) showProfile(profile Profile) {
	wille.printDefinedKeyWithValue("Email", profile.Email)
	wille.printDefinedKeyWithValue("Username", profile.Username)
	wille.printDefinedKeyWithValue("Password", profile.Password)
	// Print CustomerInfos object
	wille.printDefinedKeyWithValue("CustomerInfos", profile.CustomerInfos)
	wille.addOneTabForPrint()
	wille.printDefinedKeyWithValue("Firstname", profile.CustomerInfos.Firstname)
	wille.printDefinedKeyWithValue("Lastname", profile.CustomerInfos.Lastname)
	wille.printDefinedKeyWithValue("PhoneNumber", profile.CustomerInfos.PhoneNumber)
	wille.resetTabForPrint()
	// Print Localization object
	wille.printDefinedKeyWithValue("Localization", profile.Localization)
	wille.addOneTabForPrint()
	wille.printDefinedKeyWithValue("Country", profile.Localization.Country)
	wille.printDefinedKeyWithValue("Region", profile.Localization.Region)
	wille.printDefinedKeyWithValue("Address", profile.Localization.Address)
	wille.resetTabForPrint()
	wille.printDefinedKeyWithValue("Guid", profile.Guid)
	wille.printDefinedKeyWithValue("Role", profile.Guid)
}

// Check the content of the Profile.json file and print it
func (wille *Wille) checkAndShowProfileJsonContent(name string) error {
	profile, err := wille.checkProfileDataValidity(name)
	if err != nil {
		return err
	}

	wille.showProfile(profile)
	return nil
}
