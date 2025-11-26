package main

import (
	"log"
	"os"

	"github.com/go-vue-code/config"
	"github.com/go-vue-code/models"
	"github.com/go-vue-code/routes"
	"github.com/joho/godotenv"
)

func main() {
	// Load environment variables
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found")
	}

	// Initialize database
	config.InitDB()

	// Auto migrate the database schema
	err = config.DB.AutoMigrate(
		&models.User{},
		&models.Role{},
		&models.Permission{},
	)
	if err != nil {
		log.Fatal("Failed to migrate database:", err)
	}

	// Seed database with initial data
	seedDatabase()

	// Setup routes
	r := routes.SetupRoutes()

	// Setup admin routes
	routes.SetupAdminRoutes(r)

	// Get port from environment or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Start server
	log.Printf("Server starting on port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatal("Failed to start server: ", err)
	}
}

// seedDatabase adds initial data to the database
func seedDatabase() {
	// Check if admin user already exists
	var adminUser models.User
	result := config.DB.Where("email = ?", "admin@example.com").First(&adminUser)
	if result.Error == nil {
		log.Println("Admin user already exists")
		return
	}

	// Create admin role
	adminRole := models.Role{
		Name:        "admin",
		Description: "Administrator with full access",
	}
	config.DB.Create(&adminRole)

	// Create user role
	userRole := models.Role{
		Name:        "user",
		Description: "Regular user with limited access",
	}
	config.DB.Create(&userRole)

	// Create permissions
	permissions := []models.Permission{
		{Name: "users.view", Description: "View users"},
		{Name: "users.create", Description: "Create users"},
		{Name: "users.update", Description: "Update users"},
		{Name: "users.delete", Description: "Delete users"},
		{Name: "roles.view", Description: "View roles"},
		{Name: "roles.create", Description: "Create roles"},
		{Name: "roles.update", Description: "Update roles"},
		{Name: "roles.delete", Description: "Delete roles"},
		{Name: "permissions.view", Description: "View permissions"},
		{Name: "permissions.create", Description: "Create permissions"},
		{Name: "permissions.update", Description: "Update permissions"},
		{Name: "permissions.delete", Description: "Delete permissions"},
	}

	for _, permission := range permissions {
		config.DB.Create(&permission)
	}

	// Assign all permissions to admin role
	config.DB.Model(&adminRole).Association("Permissions").Append(&permissions)

	// Assign only view permissions to user role
	userPermissions := []models.Permission{permissions[0], permissions[4], permissions[8]} // users.view, roles.view, permissions.view
	config.DB.Model(&userRole).Association("Permissions").Append(&userPermissions)

	// Create admin user
	admin := models.User{
		Username:  "admin",
		Email:     "admin@example.com",
		Password:  "admin123", // This will be hashed automatically
		FirstName: "Admin",
		LastName:  "User",
		Active:    true,
		RoleID:    adminRole.ID,
	}
	config.DB.Create(&admin)

	log.Println("Database seeded with initial data")
}
