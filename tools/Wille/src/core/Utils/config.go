//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// config.go
//

package utils

import (
	"errors"
)

// Structure used to check environnement variable validity
type Config struct {
	DEV_DB_CLIENT          string `json:"DEV_DB_CLIENT"`
	DEV_DB_PASSWORD        string `json:"DEV_DB_PASSWORD"`
	DEV_DB_USERS_NAME      string `json:"DEV_DB_USERS_NAME"`
	DEV_DB_BOXES_NAME      string `json:"DEV_DB_BOXES_NAME"`
	DEV_DB_DEVELOPERS_NAME string `json:"DEV_DB_DEVELOPERS_NAME"`
	DEV_URI_USERS_DB       string `json:"DEV_URI_USERS_DB"`
}

func checkConfig(config *Config) error {
	if config == nil {
		return errors.New("Error: Config object nil")
	} else if config.DEV_DB_CLIENT == "" {
		return errors.New("Error: Config.DEV_DB_CLIENT empty value")
	} else if config.DEV_DB_PASSWORD == "" {
		return errors.New("Error: Config.DEV_DB_PASSWORD empty value")
	} else if config.DEV_DB_USERS_NAME == "" {
		return errors.New("Error: Config.DEV_DB_USERS_NAME empty value")
	} else if config.DEV_DB_BOXES_NAME == "" {
		return errors.New("Error: Config.DEV_DB_BOXES_NAME empty value")
	} else if config.DEV_DB_DEVELOPERS_NAME == "" {
		return errors.New("Error: Config.DEV_DB_DEVELOPERS_NAME empty value")
	} else if config.DEV_URI_USERS_DB == "" {
		return errors.New("Error: Config.DEV_URI_USERS_DB empty value")
	}
	return nil
}

func loadConfig() (*Config, error) {
	var config Config

	// Get Mandatory env variable
	decoder, err := OpenAndGenerateJsonDecoder("src/config.json")
	if err != nil {
		return nil, err
	}
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&config); err != nil {
		return nil, err
	}
	return &config, nil
}

func CheckAndLoadConfig() (*Config, error) {
	config, err := loadConfig()

	if err != nil {
		return nil, err
	}

	if err := checkConfig(config); err != nil {
		return nil, err
	}
	return config, nil
}
