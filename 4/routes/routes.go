package routes

import (
	"net/http"

	"gemini-project/controllers"
	"github.com/gin-gonic/gin"
)

// RegisterRoutes registers the application's routes
func RegisterRoutes(router *gin.Engine, userController *controllers.UserController, homeController *controllers.HomeController) {
	router.GET("/favicon.ico", func(c *gin.Context) {
		c.Status(http.StatusNoContent)
	})

	router.GET("/", homeController.ShowHome)

	router.GET("/login", userController.ShowLogin)
	router.POST("/login", userController.LoginUser)

	router.GET("/register", userController.ShowRegister)
	router.POST("/register", userController.RegisterUser)

	router.GET("/logout", userController.LogoutUser)

	// Dashboard route (protected)
	router.GET("/dashboard", homeController.ShowDashboard)
}
