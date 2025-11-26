package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/go-vue-code/controllers/admin"
	"github.com/go-vue-code/middleware"
)

// SetupAdminRoutes sets up routes for admin functionality
func SetupAdminRoutes(router *gin.Engine) {
	// Admin routes group
	adminGroup := router.Group("/api/admin")
	adminGroup.Use(middleware.AuthMiddleware())
	{
		// User management routes
		users := adminGroup.Group("/users")
		{
			users.GET("", admin.GetUsers)
			users.GET("/:id", admin.GetUser)
			users.POST("", admin.CreateUser)
			users.PUT("/:id", admin.UpdateUser)
			users.DELETE("/:id", admin.DeleteUser)
			users.POST("/:id/reset-password", admin.ResetPassword)
		}

		// Role management routes
		roles := adminGroup.Group("/roles")
		{
			roles.GET("", admin.GetRoles)
			roles.GET("/:id", admin.GetRole)
			roles.POST("", admin.CreateRole)
			roles.PUT("/:id", admin.UpdateRole)
			roles.DELETE("/:id", admin.DeleteRole)
		}

		// Permission management routes
		permissions := adminGroup.Group("/permissions")
		{
			permissions.GET("", admin.GetPermissions)
			permissions.GET("/groups", admin.GetPermissionGroups)
			permissions.GET("/:id", admin.GetPermission)
			permissions.POST("", admin.CreatePermission)
			permissions.PUT("/:id", admin.UpdatePermission)
			permissions.DELETE("/:id", admin.DeletePermission)
		}
	}
}
