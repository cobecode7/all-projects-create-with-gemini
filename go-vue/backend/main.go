package main

import (
	"github.com/gemini/go-vue/backend/auth"
	"github.com/gemini/go-vue/backend/models"
	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var db *gorm.DB
var err error

func main() {
	// Initialize the database
	db, err = gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	db.AutoMigrate(&models.User{})

	// Initialize the Gin router
	r := gin.Default()
	r.Use(gin.CORS())

	authController := auth.AuthController{DB: db}

	r.POST("/register", authController.Register)
	r.POST("/login", authController.Login)

	protected := r.Group("/protected")
	protected.Use(auth.AuthMiddleware())
	{
		protected.GET("/profile", func(c *gin.Context) {
			username := c.MustGet("username").(string)
			role := c.MustGet("role").(string)
			c.JSON(200, gin.H{
				"message":  "Welcome to the protected area!",
				"username": username,
				"role":     role,
			})
		})

		admin := protected.Group("/admin")
		admin.Use(auth.CheckRole("admin"))
		{
			admin.GET("/dashboard", func(c *gin.Context) {
				username := c.MustGet("username").(string)
				c.JSON(200, gin.H{
					"message":  "Welcome to the admin dashboard!",
					"username": username,
				})
			})
		}
	}

	// Simple route for testing
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Hello World!",
		})
	})

	// Run the server
	r.Run()
}
