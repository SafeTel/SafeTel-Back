//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package wille

// "go.mongodb.org/mongo-driver/mongo/readpref"
// "go.mongodb.org/mongo-driver/bson/primitive"

func (wille *Wille) addOneTabForPrint() {
	tabPrefixForJsonPrint += "\t"
}

func (wille *Wille) removeOneTabForPrint() {
	if len(tabPrefixForJsonPrint) >= 2 {
		tabPrefixForJsonPrint = tabPrefixForJsonPrint[2:]
	}
}

func (wille *Wille) resetTabForPrint() {
	tabPrefixForJsonPrint = "\t\t"
}

func (wille *Wille) printEmptyOrUndefinedKey(key string) {
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, key, ResetColor, "value: ", Red, "Empty or not defined", ResetColor)
}

func (wille *Wille) printDefinedKeyWithValue(key string, value interface{}) {
	InfoLogger.Println(tabPrefixForJsonPrint, Cyan, key, ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, value, ResetColor)
}

func (wille *Wille) print(key interface{}) {
	InfoLogger.Println(tabPrefixForJsonPrint, key)
}
