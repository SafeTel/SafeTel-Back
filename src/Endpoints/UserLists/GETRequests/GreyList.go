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

	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses"
	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList"
	whiteList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList"

	"github.com/labstack/echo/v4"
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
