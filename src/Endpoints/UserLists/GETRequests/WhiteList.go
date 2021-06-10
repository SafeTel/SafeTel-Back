//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// WhiteList
//

package getRequestsUserLists

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"          // MongoDB Handler
	whitelist "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList" // WhiteList Handler

	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func GetWhiteList(context echo.Context) error {

	userId := context.Param("userId")
	response := responses.GetWhiteListResponse{}

	client := db.CreateConnectionToAtlas()
	blackList := whitelist.NewWhilelist(client, os.Getenv("DBName"))

	response.WhiteList = blackList.GetWhiteListForUserId(userId).Number

	return context.JSON(http.StatusOK, response)
}
