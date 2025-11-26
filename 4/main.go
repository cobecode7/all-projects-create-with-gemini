package main

import (
	"fmt"
	"log"
	"os"

	"gemini-project/controllers"
	"gemini-project/models"
	"gemini-project/routes"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/sessions"
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func main() {
	log.Println("Starting application...")
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	log.Println("Environment variables loaded successfully")

	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable", dbHost, dbUser, dbPassword, dbName, dbPort)

	log.Printf("Attempting to connect to database with DSN: %s", dsn)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	fmt.Println("Database connection successful")

	// Migrate the schema
	db.AutoMigrate(&models.User{})
	fmt.Println("Database migration successful")

	// Set up session store
	store := sessions.NewCookieStore([]byte("secret-key"))

	// Set up Gin router
	router := gin.Default()
	router.LoadHTMLGlob("views/*")
	router.Static("/static", "./static")

	// Initialize controllers
	userController := controllers.NewUserController(db, store)
	homeController := controllers.NewHomeController(db, store)

	// Register routes
	log.Println("Registering routes...")
	routes.RegisterRoutes(router, userController, homeController)
	log.Println("Routes registered successfully")

	// Start the server
	log.Println("Starting server on port 8080...")
	router.Run(":8080")
}
