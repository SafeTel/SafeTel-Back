//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - whiteListDB.go
//

package atlasCollections

import dataModels "github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"

//  ./src/DB/WhiteListDB.go de:
//  - D'obtenir la liste des utilisateurs WhiteListés à partir de l'id d'un utilisateur
//  GetWhiteList(userId string)

//  - De WhiteLister un numéro  à partir d'un numéro à WhiteList et de l'id de l'utilisateur
//  WhiteListNumber(userId string, number string)

//  - D'enlever un numéro de la WhiteList à partir d'un numéro à WhiteList et de l'id de l'utilisateur
//  UNWhiteListNumber(userId string, number string)

func GetWhiteListForUserId(userId string) []dataModels.PhoneNumber {
	return nil
}

func AddWhiteListPhoneNumberForUserId(userId string, thePhoneNumber dataModels.PhoneNumber) {

}

func DeleteWhiteListPhoneNumberForUserId(userId string, thePhoneNumber dataModels.PhoneNumber) {

}
