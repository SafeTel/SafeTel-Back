//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - blackListDB.go
//

package atlasCollections

import "github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"

// ./src/DB/BlackListDB.go de:
// - D'obtenir la liste des utilisateurs BlackListés à partir de l'id d'un utilisateur
// GetBlackList(userId string)

// - De WhiteLister un numéro  à partir d'un numéro à BlackList et de l'id de l'utilisateur
// BlackListNumber(userId string, number string)

// - D'enlever un numéro de la BlackList à partir d'un numéro à BlackList et de l'id de l'utilisateur
// UNBlackListNumber(userId string, number string)

func GetBlacklistForUserId(userID string) []dataModels.PhoneNumber {
	return nil
}

func AddBlacklistPhoneNumberForUserId(userId string, thePhoneNumber dataModels.PhoneNumber) {

}

func DeleteBlacklistPhoneNumberForUserId(userId string, thePhoneNumber dataModels.PhoneNumber) {

}
