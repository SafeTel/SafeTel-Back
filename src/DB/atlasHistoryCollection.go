//
// SAFETEL PROJECT, 2021
// SafeTel-Backend
// File description:
// Atlas-Collections - historyDB.go
//

package atlasCollections

import "github.com/SafeTel/SafeTel-Back.git/src/DB/dataModels"

// ./src/DB/HistoryDB.go de:
// - D'obtenir l'history à partir de l'id d'un utilisateur
// GetHistory(userId string)

// - D'enlever un appel de l'history à partir d'un numéro, d'un timestamp unix, et de l'id de l'utilisateur
// UNBlackListNumber(userId string, number string, unixtimestamp int)

func GetHistoryForUserId(userId string) []dataModels.PhoneNumber {
	return nil
}
