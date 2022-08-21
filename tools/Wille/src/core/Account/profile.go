//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package profile

import (
	// Read Json
	utils "PostmanDbDataImplementation/core/Utils"
	// Show Command
	print "PostmanDbDataImplementation/core/Utils/Print"
	// Error Type
	"errors"
	// Mongo Type
	"go.mongodb.org/mongo-driver/mongo"
)

type Profile struct {
	Client         *mongo.Client
	DB             *mongo.Database
	UserCollection *mongo.Collection
	Print          *print.Print
	Data           *Data
}

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

type Data struct {
	MagicNumber   int           `json:"magicnumber"`
	Email         string        `json:"email"`
	Username      string        `json:"userName"`
	Password      string        `json:"password"`
	CustomerInfos CustomerInfos `json:"CustomerInfos"`
	Localization  Localization  `json:"Localization"`
}

// Check the content of a Profile object
func (profile *Profile) checkProfileObjectDataValidity(name string, data Data) error {

	if data.Email == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Email value")
	}
	if data.Username == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Username value")
	}
	if data.Password == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Password value")
	}
	emptyCustomerInfos := CustomerInfos{}

	if data.CustomerInfos == emptyCustomerInfos {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile CustomerInfos value")
	}
	if data.CustomerInfos.Firstname == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile CustomerInfos.Firstname value")
	}
	if data.CustomerInfos.Lastname == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile CustomerInfos.Lastname value")
	}
	if data.CustomerInfos.PhoneNumber == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile CustomerInfos.PhoneNumber value")
	}
	emptyLocalization := Localization{}

	if data.Localization == emptyLocalization {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Localization value")
	}
	if data.Localization.Country == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Localization.Country value")
	}
	if data.Localization.Region == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Localization.Region value")
	}
	if data.Localization.Address == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Localization.Address value")
	}
	return nil
}

// Check the content of the Profile.json file and check if the data has not been uploaded yet
func (profile *Profile) checkProfileDataValidity(name string) (Data, error) {
	var data Data

	decoder, err := utils.OpenAndGenerateJsonDecoder("data/" + name + "/Profile.json")
	if err != nil {
		return Data{}, err
	}
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&data); err != nil {
		return Data{}, err
	}
	// check Json Content
	if err = profile.checkProfileObjectDataValidity(name, data); err != nil {
		return Data{}, err
	}
	return data, nil
}

func (profile *Profile) setData(name string) error {
	data, err := profile.checkProfileDataValidity(name)

	if err != nil {
		return err
	}
	profile.Data = &data
	return nil
}

func (profile *Profile) LoadData(name string) error {
	return profile.setData(name)
}

// // Upload the Profile.json file
// func (profile *Profile) UploadProfileFile(name string) error {
// 	data, err := profile.checkProfileDataValidity(name)

// 	if err != nil {
// 		return err
// 	}
// 	// TODO: replace start
// 	// Generating a bson filter using the value of guid
// 	filter := bson.M{"email": data.Email, "guid": data.Guid}
// 	if err = utils.CheckDataNotExistInCollection(profile.UserCollection, filter); err != nil {
// 		profile.Print.Info("Profile.json data of model " + name + " already exist inside the server")
// 		return nil
// 	}
// 	// Upload
// 	err, inOut, inErr := mongoUtils.Import(profile.DEV_URI_USERS_DB, "User", "data/"+name+"/Profile.json")

// 	if err != nil {
// 		profile.Print.Info("Profile.json data of model " + name + " already exist inside the server")
// 		return err
// 	}
// 	// TODO: replace end
// 	profile.Print.Info("StdOut: Uploading the profile file of " + name + ": " + inOut)
// 	profile.Print.Info("StdErr: Uploading the profile file of " + name + ": " + inErr)
// 	return nil
// }

func (profile *Profile) ShowProfile() {

	profile.Print.ResetTabForPrint()
	profile.Print.Info("\t- Profile.json Content:")
	// Print Data
	profile.Print.DefinedKeyWithValueWithTab("Email", profile.Data.Email)
	profile.Print.DefinedKeyWithValueWithTab("Username", profile.Data.Username)
	profile.Print.DefinedKeyWithValueWithTab("Password", profile.Data.Password)
	// Print CustomerInfos object
	profile.Print.DefinedKeyWithValueWithTab("CustomerInfos", profile.Data.CustomerInfos)
	profile.Print.AddOneTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Firstname", profile.Data.CustomerInfos.Firstname)
	profile.Print.DefinedKeyWithValueWithTab("Lastname", profile.Data.CustomerInfos.Lastname)
	profile.Print.DefinedKeyWithValueWithTab("PhoneNumber", profile.Data.CustomerInfos.PhoneNumber)
	profile.Print.ResetTabForPrint()
	// Print Localization object
	profile.Print.DefinedKeyWithValueWithTab("Localization", profile.Data.Localization)
	profile.Print.AddOneTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Country", profile.Data.Localization.Country)
	profile.Print.DefinedKeyWithValueWithTab("Region", profile.Data.Localization.Region)
	profile.Print.DefinedKeyWithValueWithTab("Address", profile.Data.Localization.Address)
	profile.Print.ResetTabForPrint()
}

func New(client *mongo.Client, print *print.Print) (*Profile, error) {
	if client == nil {
		return nil, errors.New("Mongo.Client object nil")
	} else if print == nil {
		return nil, errors.New("Print object nil")
	}

	profile := Profile{Client: client}
	profile.DB = profile.Client.Database("Melchior")
	profile.UserCollection = profile.DB.Collection("User")
	profile.Print = print
	profile.Data = nil

	return &profile, nil
}
