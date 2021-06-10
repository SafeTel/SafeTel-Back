//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// BlackList
//

package getRequestsUserLists

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	blackList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/BlackList" // BlackList Handler
	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"          // MongoDB Handler

	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func GetBlackList(context echo.Context) error {

	userId := context.Param("userId")
	response := responses.GetBlackListResponse{}

	client := db.CreateConnectionToAtlas()
	blackList := blackList.NewBlacklist(client, os.Getenv("DBName"))

	response.BlackList = blackList.GetBlacklistForUserId(userId).Number

	return context.JSON(http.StatusOK, response)
}
