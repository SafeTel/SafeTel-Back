//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package profile

import (
	utils "PostmanDbDataImplementation/core/Utils"
	mongoUtils "PostmanDbDataImplementation/core/Utils/Mongo"
	print "PostmanDbDataImplementation/core/Utils/Print"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type Profile struct {
	Client            *mongo.Client
	DB                *mongo.Database
	UserCollection    *mongo.Collection
	Print             *print.Print
	DEV_DB_USERS_NAME string
	DEV_URI_USERS_DB  string
}

type Administrative struct {
	Passwordlost bool `json:"passwordlost"`
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
	Email          string         `json:"email"`
	Username       string         `json:"userName"`
	Password       string         `json:"password"`
	CustomerInfos  CustomerInfos  `json:"CustomerInfos"`
	Localization   Localization   `json:"Localization"`
	Administrative Administrative `json:"Administrative"`
	Guid           string         `json:"guid"`
	Role           string         `json:"role"`
	Time           float64        `json:"time"`
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
	if data.Guid == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Guid value")
	}
	if data.Role == "" {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Role value")
	}
	if data.Time == 0 {
		return errors.New("Problem with json file " + name + "/Lists/Profile.jsonBox Missing Profile Time value")
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

// Upload the Profile.json file
func (profile *Profile) UploadProfileFile(name string) error {
	data, err := profile.checkProfileDataValidity(name)

	if err != nil {
		return err
	}
	// Generating a bson filter using the value of guid
	filter := bson.M{"email": data.Email, "guid": data.Guid}
	if err = utils.CheckDataValidityOnStorage(profile.UserCollection, filter); err != nil {
		profile.Print.Info("Profile.json data of model " + name + " already exist inside the server")
		return nil
	}
	// Upload
	err, inOut, inErr := mongoUtils.Import(profile.DEV_URI_USERS_DB, "User", "data/"+name+"/Profile.json")

	if err != nil {
		profile.Print.Info("Profile.json data of model " + name + " already exist inside the server")
		return err
	}
	profile.Print.Info("StdOut: Uploading the profile file of " + name + ": " + inOut)
	profile.Print.Info("StdErr: Uploading the profile file of " + name + ": " + inErr)
	return nil
}

func (profile *Profile) showProfile(data Data) {
	profile.Print.DefinedKeyWithValueWithTab("Email", data.Email)
	profile.Print.DefinedKeyWithValueWithTab("Username", data.Username)
	profile.Print.DefinedKeyWithValueWithTab("Password", data.Password)
	// Print CustomerInfos object
	profile.Print.DefinedKeyWithValueWithTab("CustomerInfos", data.CustomerInfos)
	profile.Print.AddOneTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Firstname", data.CustomerInfos.Firstname)
	profile.Print.DefinedKeyWithValueWithTab("Lastname", data.CustomerInfos.Lastname)
	profile.Print.DefinedKeyWithValueWithTab("PhoneNumber", data.CustomerInfos.PhoneNumber)
	profile.Print.ResetTabForPrint()
	// Print Localization object
	profile.Print.DefinedKeyWithValueWithTab("Localization", data.Localization)
	profile.Print.AddOneTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Country", data.Localization.Country)
	profile.Print.DefinedKeyWithValueWithTab("Region", data.Localization.Region)
	profile.Print.DefinedKeyWithValueWithTab("Address", data.Localization.Address)
	profile.Print.ResetTabForPrint()
	// Print Administrative object
	profile.Print.DefinedKeyWithValueWithTab("Administrative", data.Administrative)
	profile.Print.AddOneTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Passwordlost", data.Administrative.Passwordlost)
	profile.Print.ResetTabForPrint()
	profile.Print.DefinedKeyWithValueWithTab("Guid", data.Guid)
	profile.Print.DefinedKeyWithValueWithTab("Role", data.Guid)
}

// Check the content of the Profile.json file and print it
func (profile *Profile) CheckAndShowProfileJsonContent(name string) error {
	data, err := profile.checkProfileDataValidity(name)
	if err != nil {
		return err
	}

	profile.showProfile(data)
	return nil
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

	config, err := utils.CheckAndLoadConfig()

	if err != nil {
		return nil, err
	}
	profile.DEV_DB_USERS_NAME = config.DEV_DB_USERS_NAME
	profile.DEV_URI_USERS_DB = config.DEV_URI_USERS_DB

	return &profile, nil
}
