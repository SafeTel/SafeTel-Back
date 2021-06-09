//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// BlackList
//

package postRequestsUserLists

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"          // MongoDB Handler
	whiteList "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/WhiteList" // WhiteList Handler

	params "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Params"       // Data Models for params
	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func PostWhiteList(context echo.Context) error {

	param := params.GenericControlList{}
	response := responses.GetBlackListResponse{}

	decoder := json.NewDecoder(context.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&param); err != nil {
		log.Println(err)
		return err
	}

	client := db.CreateConnectionToAtlas()
	whitelist := whiteList.NewWhilelist(client, os.Getenv("DBName"))

	whitelist.AddWhitelistPhoneNumberForUserId(param.UserId, param.Number)

	response.BlackList = whitelist.GetWhiteListForUserId(param.UserId).Number

	return context.JSON(http.StatusOK, response)
}
