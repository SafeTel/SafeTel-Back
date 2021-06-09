//
// SAFETEL PROJECT, 2021
// SafeTel-Back
// File description:
// History
//

package getRequestsUserLists

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"

	db "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/Connect"      // MongoDB Handler
	history "github.com/SafeTel/SafeTel-Back.git/src/ExternalServices/AtlasDB/History" // History Handler

	responses "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/Models/Responses" // Data Models for responses
)

func GetHistory(context echo.Context) error {

	userId := context.Param("userId")
	response := responses.GetHistoryResponse{}

	client := db.CreateConnectionToAtlas()
	history := history.NewHistory(client, os.Getenv("DBName"))

	response.Values = history.GetHistoryForUserId(userId).Values

	return context.JSON(http.StatusOK, response)
}
