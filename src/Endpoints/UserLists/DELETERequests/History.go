//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// History
//

package deleteRequestsUserLists

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"      // MongoDB Handler
	history "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/History" // History Handler

	params "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Params"       // Data Models for params
	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func DeleteHistory(context echo.Context) error {

	param := params.DeleteHistory{}
	response := responses.GetHistoryResponse{}

	decoder := json.NewDecoder(context.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&param); err != nil {
		log.Println(err)
		return err
	}

	client := db.CreateConnectionToAtlas()
	history := history.NewHistory(client, os.Getenv("DBName"))

	history.DelHistoryCallForUserId(param.UserId, param.Number, param.Time)

	response.Values = history.GetHistoryForUserId(param.UserId).Values

	return context.JSON(http.StatusOK, response)
}
