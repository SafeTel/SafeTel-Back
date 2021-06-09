//
// EPITECH PROJECT, 2021
// SafeTel-Back
// File description:
// GreyList
//

package getRequestsUserLists

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect" // MongoDB Handler

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList" // BlackList Handler
	whiteList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList" // WhiteList Handler

	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func GetGreyList(context echo.Context) error {

	userId := context.Param("userId")
	response := responses.GetGreyListResponse{}

	client := db.CreateConnectionToAtlas()
	blacklist := blackList.NewBlacklist(client, os.Getenv("DBName"))
	whitelist := whiteList.NewWhilelist(client, os.Getenv("DBName"))

	response.BlackList = blacklist.GetBlacklistForUserId(userId).Number
	response.Whitelist = whitelist.GetWhiteListForUserId(userId).Number

	return context.JSON(http.StatusOK, response)
}
