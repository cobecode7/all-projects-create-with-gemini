package router

import (
	"github.com/gin-gonic/gin"
	"github.com/yourusername/ecommerce-go/internal/handlers"
)

func SetupRoutes(r *gin.Engine, authHandler *handlers.AuthHandler) {
	api := r.Group("/api")
	auth := api.Group("/auth")
	{
		auth.POST("/register", authHandler.Register)
		auth.POST("/login", authHandler.Login)
	}
}
