#!/usr/bin/env bash
set -e

echo "🚀 Starting Go E-commerce project setup..."

# Root folder
PROJECT_NAME="ecommerce-go"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# ────────────────────────────────
# 1. Create folders
# ────────────────────────────────
echo "📁 Creating folder structure..."

mkdir -p cmd/server
mkdir -p internal/{config,database,models,repository,handlers,router,utils}
mkdir -p migrations
mkdir -p tests

# ────────────────────────────────
# 2. Initialize Go module
# ────────────────────────────────
echo "🧩 Initializing go module..."
go mod init github.com/yourusername/ecommerce-go
go get github.com/jmoiron/sqlx
go get github.com/lib/pq
go get github.com/golang-jwt/jwt/v5
go get github.com/go-playground/validator/v10
go get github.com/rs/zerolog/log
go get github.com/rs/zerolog
go get github.com/gin-gonic/gin

# ────────────────────────────────
# 3. Create config.go
# ────────────────────────────────
cat <<'EOF' > internal/config/config.go
package config

import (
	"log"
	"os"
)

type Config struct {
	DBUrl      string
	JWTSecret  string
	ServerPort string
}

func LoadConfig() *Config {
	cfg := &Config{
		DBUrl:      getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/ecommerce?sslmode=disable"),
		JWTSecret:  getEnv("JWT_SECRET", "supersecretkey"),
		ServerPort: getEnv("PORT", "8080"),
	}

	log.Println("✅ Config loaded successfully")
	return cfg
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}
EOF

# ────────────────────────────────
# 4. Create database.go
# ────────────────────────────────
cat <<'EOF' > internal/database/database.go
package database

import (
	"log"
	"time"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

func NewConnection(dbURL string) *sqlx.DB {
	db, err := sqlx.Connect("postgres", dbURL)
	if err != nil {
		log.Fatalf("❌ Failed to connect to database: %v", err)
	}

	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(25)
	db.SetConnMaxLifetime(5 * time.Minute)

	log.Println("✅ Database connected successfully")
	return db
}
EOF

# ────────────────────────────────
# 5. Create user.go
# ────────────────────────────────
cat <<'EOF' > internal/models/user.go
package models

import "time"

type User struct {
	ID        int64     `db:"id" json:"id"`
	Name      string    `db:"name" json:"name" validate:"required,min=2"`
	Email     string    `db:"email" json:"email" validate:"required,email"`
	Password  string    `db:"password" json:"password,omitempty" validate:"required"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
	UpdatedAt time.Time `db:"updated_at" json:"updated_at"`
}
EOF

# ────────────────────────────────
# 6. Create user_repository.go
# ────────────────────────────────
cat <<'EOF' > internal/repository/user_repository.go
package repository

import (
	"errors"

	"github.com/jmoiron/sqlx"
	"github.com/yourusername/ecommerce-go/internal/models"
)

type UserRepository struct {
	DB *sqlx.DB
}

func NewUserRepository(db *sqlx.DB) *UserRepository {
	return &UserRepository{DB: db}
}

func (r *UserRepository) Create(user *models.User) error {
	query := `INSERT INTO users (name, email, password, created_at, updated_at)
	          VALUES ($1, $2, $3, NOW(), NOW()) RETURNING id`
	err := r.DB.QueryRow(query, user.Name, user.Email, user.Password).Scan(&user.ID)
	if err != nil {
		return err
	}
	return nil
}

func (r *UserRepository) FindByEmail(email string) (*models.User, error) {
	var user models.User
	err := r.DB.Get(&user, "SELECT * FROM users WHERE email = $1", email)
	if err != nil {
		return nil, errors.New("user not found")
	}
	return &user, nil
}
EOF

# ────────────────────────────────
# 7. Create auth_handler.go
# ────────────────────────────────
cat <<'EOF' > internal/handlers/auth_handler.go
package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/yourusername/ecommerce-go/internal/models"
	"github.com/yourusername/ecommerce-go/internal/repository"
	"github.com/yourusername/ecommerce-go/internal/utils"
)

type AuthHandler struct {
	Repo      *repository.UserRepository
	Validator *validator.Validate
}

func NewAuthHandler(repo *repository.UserRepository) *AuthHandler {
	return &AuthHandler{
		Repo:      repo,
		Validator: validator.New(),
	}
}

func (h *AuthHandler) Register(c *gin.Context) {
	var input models.User
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.Validator.Struct(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"validation_error": err.Error()})
		return
	}

	hashed, _ := utils.HashPassword(input.Password)
	input.Password = hashed

	if err := h.Repo.Create(&input); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "User created", "user": input})
}

func (h *AuthHandler) Login(c *gin.Context) {
	var input struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := h.Repo.FindByEmail(input.Email)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
		return
	}

	if !utils.CheckPasswordHash(input.Password, user.Password) {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
		return
	}

	token, err := utils.GenerateJWT(user.Email)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"token": token})
}
EOF

# ────────────────────────────────
# 8. Create jwt + password utils
# ────────────────────────────────
cat <<'EOF' > internal/utils/jwt.go
package utils

import (
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtKey = []byte("supersecretkey")

func GenerateJWT(email string) (string, error) {
	claims := jwt.MapClaims{
		"email": email,
		"exp":   time.Now().Add(time.Hour * 24).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtKey)
}
EOF

cat <<'EOF' > internal/utils/password.go
package utils

import "golang.org/x/crypto/bcrypt"

func HashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	return string(bytes), err
}

func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}
EOF

# ────────────────────────────────
# 9. Router setup
# ────────────────────────────────
cat <<'EOF' > internal/router/router.go
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
EOF

# ────────────────────────────────
# 10. main.go
# ────────────────────────────────
cat <<'EOF' > cmd/server/main.go
package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/yourusername/ecommerce-go/internal/config"
	"github.com/yourusername/ecommerce-go/internal/database"
	"github.com/yourusername/ecommerce-go/internal/handlers"
	"github.com/yourusername/ecommerce-go/internal/repository"
	"github.com/yourusername/ecommerce-go/internal/router"
)

func main() {
	cfg := config.LoadConfig()
	db := database.NewConnection(cfg.DBUrl)
	defer db.Close()

	userRepo := repository.NewUserRepository(db)
	authHandler := handlers.NewAuthHandler(userRepo)

	r := gin.Default()
	router.SetupRoutes(r, authHandler)

	srv := &http.Server{
		Addr:    ":" + cfg.ServerPort,
		Handler: r,
	}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("❌ Server error: %v", err)
		}
	}()

	log.Println("🚀 Server running on port", cfg.ServerPort)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt)
	<-quit

	log.Println("🧹 Gracefully shutting down...")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("✅ Server exited cleanly")
}
EOF

# ────────────────────────────────
# 11. Migration file
# ────────────────────────────────
cat <<'EOF' > migrations/001_create_users_table.sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
EOF

echo "✅ Project $PROJECT_NAME created successfully!"
EOF

---

### 🧩 الاستخدام:
```bash
#chmod +x setup_ecommerce_go.sh
#./setup_ecommerce_go.sh
