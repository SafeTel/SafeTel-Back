//
// EPITECH PROJECT, 2021
// SafeTel-Back
// File description:
// main
//

// Utility: This file is only here to instanciate routes and launch the server

package main

import (
	"github.com/labstack/echo/v4" // Echo framework

	getRequests "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/GETRequests"
)

func initUserLists(echoServer *echo.Echo) {

	/* GET Requests */
	echoServer.GET("/get/blacklist/:userId", getRequests.GetBlackList)
	echoServer.GET("/get/whitelist/:userId", getRequests.GetWhiteList)
	echoServer.GET("/get/history/:userId", getRequests.GetHistory)
	echoServer.GET("/get/greylist/:userId", getRequests.GetGreyList)

}

func main() {

	echoServer := echo.New() // Create a new object Echo server

	initUserLists(echoServer) // Init routes for UserLists

	echoServer.Logger.Fatal(echoServer.Start(":2407")) // Launch Echo Server
}
