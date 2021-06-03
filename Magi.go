//
// EPITECH PROJECT, 2021
// SafeTel-Back
// File description:
// main
//

// Utility: This file is only here to instanciate routes and launch the server

package main

import (
	"net/http"

	"github.com/labstack/echo/v4" // Echo framework
)

func main() {

	echoServer := echo.New() // Create a new object Echo server

	echoServer.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Welcome to Magi!") // Proof of working
	})

	echoServer.Logger.Fatal(echoServer.Start(":2407")) // Launch Echo Server
}
