//
// SAFETEL PROJECT, 2022
// SafeTel-Back
// File description:
// wille
//

package print

import (
	"log" // Logging
	"os"  // I/O: stdin - stdout
)

// "go.mongodb.org/mongo-driver/mongo/readpref"
// "go.mongodb.org/mongo-driver/bson/primitive"

type Print struct {
	TabPrefixForJsonPrint string
	WarningLogger         *log.Logger
	InfoLogger            *log.Logger
	ErrorLogger           *log.Logger
}

func (print *Print) AddOneTabForPrint() {
	print.TabPrefixForJsonPrint += "\t"
}

func (print *Print) RemoveOneTabForPrint() {
	if len(print.TabPrefixForJsonPrint) >= 2 {
		print.TabPrefixForJsonPrint = print.TabPrefixForJsonPrint[2:]
	}
}

func (print *Print) ResetTabForPrint() {
	print.TabPrefixForJsonPrint = "\t\t"
}

func (print *Print) EmptyOrUndefinedKeyWithTab(key string) {
	var ResetColor = "\033[0m"
	var Red = "\033[31m"
	var Cyan = "\033[36m"

	print.InfoLogger.Println(print.TabPrefixForJsonPrint, Cyan, key, ResetColor, "value: ", Red, "Empty or not defined", ResetColor)
}

func (print *Print) DefinedKeyWithValueWithTab(key string, value interface{}) {
	var ResetColor = "\033[0m"
	var Cyan = "\033[36m"
	var Green = "\033[32m"

	print.InfoLogger.Println(print.TabPrefixForJsonPrint, Cyan, key, ResetColor, "value: ", Green, "defined", ResetColor, "Value: ", Cyan, value, ResetColor)
}

func (print *Print) InfoWithTab(key interface{}) {
	print.InfoLogger.Println(print.TabPrefixForJsonPrint, key)
}

func (print *Print) Info(key interface{}) {
	print.InfoLogger.Println(key)
}

func (print *Print) WarningWithTab(key interface{}) {
	print.WarningLogger.Println(print.TabPrefixForJsonPrint, key)
}

func (print *Print) Warning(key interface{}) {
	print.WarningLogger.Println(key)
}

func (print *Print) ErrorWithTab(key interface{}) {
	print.ErrorLogger.Println(print.TabPrefixForJsonPrint, key)
}

func (print *Print) Error(key interface{}) {
	print.ErrorLogger.Println(key)
}

func New() *Print {
	var print Print

	print.TabPrefixForJsonPrint = "\t\t"

	print.InfoLogger = log.New(os.Stdin, "", log.Ldate|log.Ltime)
	print.WarningLogger = log.New(os.Stderr, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	print.ErrorLogger = log.New(os.Stderr, "ERROR: ", log.Ldate|log.Ltime|log.Lmicroseconds|log.Lshortfile)

	return &print
}
