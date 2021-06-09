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

	getUserListsRequests "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/GETRequests"   // GET Requests for User Lists
	postUserListsRequests "github.com/SafeTel/SafeTel-Back.git/src/Endpoints/UserLists/POSTRequests" // POST Requests for User Lists
)

func initUserLists(echoServer *echo.Echo) {

	/* GET Requests */
	echoServer.GET("/user/blacklist/:userId", getUserListsRequests.GetBlackList)
	echoServer.GET("/user/whitelist/:userId", getUserListsRequests.GetWhiteList)
	echoServer.GET("/user/history/:userId", getUserListsRequests.GetHistory)
	echoServer.GET("/user/greylist/:userId", getUserListsRequests.GetGreyList)

	/* POST Requests*/
	echoServer.POST("/user/blacklist", postUserListsRequests.PostBlackList)
	echoServer.POST("/user/whitelist", postUserListsRequests.PostWhiteList)
}

func main() {

	echoServer := echo.New() // Create a new object Echo server

	initUserLists(echoServer) // Init routes for UserLists

	echoServer.Logger.Fatal(echoServer.Start(":2407")) // Launch Echo Server
}
