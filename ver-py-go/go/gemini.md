سخة Backend بلغة Go
📁 هيكل المشروع Go
text

ecommerce-go/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── database/
│   │   └── database.go
│   ├── models/
│   │   ├── user.go
│   │   ├── product.go
│   │   └── order.go
│   ├── handlers/
│   │   ├── auth.go
│   │   ├── users.go
│   │   ├── products.go
│   │   └── orders.go
│   ├── middleware/
│   │   ├── auth.go
│   │   └── cors.go
│   ├── utils/
│   │   ├── jwt.go
│   │   └── password.go
│   └── repository/
│       ├── user_repo.go
│       ├── product_repo.go
│       └── order_repo.go
├── pkg/
│   └── response/
│       └── response.go
├── api/
│   └── docs/
├── migrations/
│   └── 001_init.sql
├── go.mod
├── go.sum
├── Dockerfile
├── docker-compose.yml
└── README.md

🐹 ملفات Go الأساسية
cmd/server/main.go
go

package main

import (
	"log"
	"net/http"
	"os"
	
	"ecommerce/internal/config"
	"ecommerce/internal/database"
	"ecommerce/internal/handlers"
	"ecommerce/internal/middleware"
	
	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

func main() {
	// Load configuration
	cfg := config.Load()
	
	// Initialize database
	db, err := database.NewConnection(cfg.DatabaseURL)
	if err != nil {
		log.Fatal("Could not connect to database:", err)
	}
	defer db.Close()
	
	// Create router
	router := mux.NewRouter()
	
	// Middleware
	router.Use(middleware.CORS)
	router.Use(middleware.Logging)
	
	// Health check
	router.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		handlers.RespondWithJSON(w, http.StatusOK, map[string]string{"status": "healthy"})
	}).Methods("GET")
	
	// API routes
	api := router.PathPrefix("/api").Subrouter()
	
	// Auth routes
	auth := api.PathPrefix("/auth").Subrouter()
	auth.HandleFunc("/register", handlers.Register).Methods("POST")
	auth.HandleFunc("/login", handlers.Login).Methods("POST")
	
	// Users routes
	users := api.PathPrefix("/users").Subrouter()
	users.Use(middleware.AuthMiddleware)
	users.HandleFunc("/me", handlers.GetCurrentUser).Methods("GET")
	users.HandleFunc("/me", handlers.UpdateUser).Methods("PUT")
	
	// Products routes
	products := api.PathPrefix("/products").Subrouter()
	products.HandleFunc("/", handlers.GetProducts).Methods("GET")
	products.HandleFunc("/{id}", handlers.GetProduct).Methods("GET")
	
	// Protected product routes
	protectedProducts := api.PathPrefix("/products").Subrouter()
	protectedProducts.Use(middleware.AuthMiddleware)
	protectedProducts.HandleFunc("/", handlers.CreateProduct).Methods("POST")
	protectedProducts.HandleFunc("/{id}", handlers.UpdateProduct).Methods("PUT")
	
	// Orders routes
	orders := api.PathPrefix("/orders").Subrouter()
	orders.Use(middleware.AuthMiddleware)
	orders.HandleFunc("/", handlers.CreateOrder).Methods("POST")
	orders.HandleFunc("/", handlers.GetUserOrders).Methods("GET")
	orders.HandleFunc("/{id}", handlers.GetOrder).Methods("GET")
	
	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	
	log.Printf("Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, router))
}

internal/config/config.go
go

package config

import (
	"os"
)

type Config struct {
	DatabaseURL    string
	JWTSecret      string
	Port           string
	AllowedOrigins []string
}

func Load() *Config {
	return &Config{
		DatabaseURL:    getEnv("DATABASE_URL", "postgresql://user:password@localhost/ecommerce?sslmode=disable"),
		JWTSecret:      getEnv("JWT_SECRET", "your-jwt-secret"),
		Port:           getEnv("PORT", "8080"),
		AllowedOrigins: []string{"http://localhost:3000", "http://127.0.0.1:3000"},
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

internal/database/database.go
go

package database

import (
	"database/sql"
	"fmt"
	"log"
	
	_ "github.com/lib/pq"
)

type DB struct {
	*sql.DB
}

func NewConnection(connString string) (*DB, error) {
	db, err := sql.Open("postgres", connString)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %w", err)
	}
	
	if err = db.Ping(); err != nil {
		return nil, fmt.Errorf("could not ping database: %w", err)
	}
	
	log.Println("Connected to database successfully")
	return &DB{db}, nil
}

func (db *DB) Close() error {
	return db.DB.Close()
}

internal/models/user.go
go

package models

import (
	"time"
	
	"golang.org/x/crypto/bcrypt"
)

type UserRole string

const (
	AdminRole   UserRole = "admin"
	VendorRole  UserRole = "vendor"
	CustomerRole UserRole = "customer"
)

type User struct {
	ID           int64     `json:"id" db:"id"`
	Email        string    `json:"email" db:"email"`
	PasswordHash string    `json:"-" db:"password_hash"`
	FirstName    string    `json:"first_name" db:"first_name"`
	LastName     string    `json:"last_name" db:"last_name"`
	Phone        *string   `json:"phone,omitempty" db:"phone"`
	IsActive     bool      `json:"is_active" db:"is_active"`
	Role         UserRole  `json:"role" db:"role"`
	CreatedAt    time.Time `json:"created_at" db:"created_at"`
	UpdatedAt    time.Time `json:"updated_at" db:"updated_at"`
}

func (u *User) SetPassword(password string) error {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.PasswordHash = string(hash)
	return nil
}

func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.PasswordHash), []byte(password))
	return err == nil
}

type UserCreateRequest struct {
	Email     string   `json:"email" validate:"required,email"`
	Password  string   `json:"password" validate:"required,min=6"`
	FirstName string   `json:"first_name" validate:"required"`
	LastName  string   `json:"last_name" validate:"required"`
	Phone     *string  `json:"phone,omitempty"`
	Role      UserRole `json:"role" validate:"oneof=admin vendor customer"`
}

type UserUpdateRequest struct {
	FirstName *string `json:"first_name,omitempty"`
	LastName  *string `json:"last_name,omitempty"`
	Phone     *string `json:"phone,omitempty"`
	IsActive  *bool   `json:"is_active,omitempty"`
}

type LoginRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type AuthResponse struct {
	Token string `json:"token"`
	User  *User  `json:"user"`
}

internal/models/product.go
go

package models

import "time"

type Product struct {
	ID           int64     `json:"id" db:"id"`
	Name         string    `json:"name" db:"name"`
	Description  *string   `json:"description,omitempty" db:"description"`
	Price        float64   `json:"price" db:"price"`
	ComparePrice *float64  `json:"compare_price,omitempty" db:"compare_price"`
	Cost         *float64  `json:"cost,omitempty" db:"cost"`
	SKU          string    `json:"sku" db:"sku"`
	Barcode      *string   `json:"barcode,omitempty" db:"barcode"`
	TrackQuantity bool     `json:"track_quantity" db:"track_quantity"`
	Quantity     int       `json:"quantity" db:"quantity"`
	IsActive     bool      `json:"is_active" db:"is_active"`
	IsDigital    bool      `json:"is_digital" db:"is_digital"`
	VendorID     int64     `json:"vendor_id" db:"vendor_id"`
	CategoryID   *int64    `json:"category_id,omitempty" db:"category_id"`
	CreatedAt    time.Time `json:"created_at" db:"created_at"`
	UpdatedAt    time.Time `json:"updated_at" db:"updated_at"`
	
	// Relations
	Vendor   *User     `json:"vendor,omitempty"`
	Category *Category `json:"category,omitempty"`
}

type Category struct {
	ID          int64     `json:"id" db:"id"`
	Name        string    `json:"name" db:"name"`
	Description *string   `json:"description,omitempty" db:"description"`
	IsActive    bool      `json:"is_active" db:"is_active"`
	ParentID    *int64    `json:"parent_id,omitempty" db:"parent_id"`
	CreatedAt   time.Time `json:"created_at" db:"created_at"`
	UpdatedAt   time.Time `json:"updated_at" db:"updated_at"`
}

type ProductCreateRequest struct {
	Name         string   `json:"name" validate:"required"`
	Description  *string  `json:"description,omitempty"`
	Price        float64  `json:"price" validate:"required,min=0"`
	ComparePrice *float64 `json:"compare_price,omitempty"`
	Cost         *float64 `json:"cost,omitempty"`
	SKU          string   `json:"sku" validate:"required"`
	Barcode      *string  `json:"barcode,omitempty"`
	TrackQuantity bool    `json:"track_quantity"`
	Quantity     int      `json:"quantity"`
	IsActive     bool     `json:"is_active"`
	IsDigital    bool     `json:"is_digital"`
	CategoryID   *int64   `json:"category_id,omitempty"`
}

type ProductUpdateRequest struct {
	Name         *string  `json:"name,omitempty"`
	Description  *string  `json:"description,omitempty"`
	Price        *float64 `json:"price,omitempty"`
	ComparePrice *float64 `json:"compare_price,omitempty"`
	Cost         *float64 `json:"cost,omitempty"`
	Barcode      *string  `json:"barcode,omitempty"`
	TrackQuantity *bool   `json:"track_quantity,omitempty"`
	Quantity     *int     `json:"quantity,omitempty"`
	IsActive     *bool    `json:"is_active,omitempty"`
	CategoryID   *int64   `json:"category_id,omitempty"`
}

internal/models/order.go
go

package models

import "time"

type OrderStatus string
type PaymentStatus string

const (
	OrderPending    OrderStatus = "pending"
	OrderConfirmed  OrderStatus = "confirmed"
	OrderProcessing OrderStatus = "processing"
	OrderShipped    OrderStatus = "shipped"
	OrderDelivered  OrderStatus = "delivered"
	OrderCancelled  OrderStatus = "cancelled"
	OrderRefunded   OrderStatus = "refunded"
	
	PaymentPending PaymentStatus = "pending"
	PaymentPaid    PaymentStatus = "paid"
	PaymentFailed  PaymentStatus = "failed"
	PaymentRefunded PaymentStatus = "refunded"
)

type Order struct {
	ID            int64        `json:"id" db:"id"`
	OrderNumber   string       `json:"order_number" db:"order_number"`
	Total         float64      `json:"total" db:"total"`
	Subtotal      float64      `json:"subtotal" db:"subtotal"`
	Tax           float64      `json:"tax" db:"tax"`
	Shipping      float64      `json:"shipping" db:"shipping"`
	Discount      float64      `json:"discount" db:"discount"`
	Status        OrderStatus  `json:"status" db:"status"`
	PaymentStatus PaymentStatus `json:"payment_status" db:"payment_status"`
	CustomerID    int64        `json:"customer_id" db:"customer_id"`
	ShippingAddress string     `json:"shipping_address" db:"shipping_address"`
	BillingAddress  string     `json:"billing_address" db:"billing_address"`
	CreatedAt     time.Time   `json:"created_at" db:"created_at"`
	UpdatedAt     time.Time   `json:"updated_at" db:"updated_at"`
	
	// Relations
	Customer *User       `json:"customer,omitempty"`
	Items    []OrderItem `json:"items,omitempty"`
}

type OrderItem struct {
	ID        int64   `json:"id" db:"id"`
	OrderID   int64   `json:"order_id" db:"order_id"`
	ProductID int64   `json:"product_id" db:"product_id"`
	Quantity  int     `json:"quantity" db:"quantity"`
	Price     float64 `json:"price" db:"price"`
	Total     float64 `json:"total" db:"total"`
	
	// Relations
	Product *Product `json:"product,omitempty"`
}

type OrderCreateRequest struct {
	ShippingAddress string             `json:"shipping_address" validate:"required"`
	BillingAddress  string             `json:"billing_address" validate:"required"`
	Items           []OrderItemRequest `json:"items" validate:"required,min=1"`
}

type OrderItemRequest struct {
	ProductID int64 `json:"product_id" validate:"required"`
	Quantity  int   `json:"quantity" validate:"required,min=1"`
}

type OrderUpdateRequest struct {
	Status        *OrderStatus  `json:"status,omitempty"`
	PaymentStatus *PaymentStatus `json:"payment_status,omitempty"`
	ShippingAddress *string     `json:"shipping_address,omitempty"`
}

internal/utils/jwt.go
go

package utils

import (
	"time"
	
	"github.com/dgrijalva/jwt-go"
	"ecommerce/internal/config"
)

type Claims struct {
	UserID int64 `json:"user_id"`
	Email  string `json:"email"`
	Role   string `json:"role"`
	jwt.StandardClaims
}

func GenerateToken(userID int64, email, role string) (string, error) {
	cfg := config.Load()
	
	expirationTime := time.Now().Add(24 * time.Hour)
	claims := &Claims{
		UserID: userID,
		Email:  email,
		Role:   role,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
			IssuedAt:  time.Now().Unix(),
		},
	}
	
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(cfg.JWTSecret))
}

func VerifyToken(tokenString string) (*Claims, error) {
	cfg := config.Load()
	
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(cfg.JWTSecret), nil
	})
	
	if err != nil {
		return nil, err
	}
	
	if !token.Valid {
		return nil, jwt.ErrSignatureInvalid
	}
	
	return claims, nil
}

internal/handlers/auth.go
go

package handlers

import (
	"database/sql"
	"net/http"
	
	"ecommerce/internal/models"
	"ecommerce/internal/utils"
	"ecommerce/pkg/response"
	
	"github.com/gorilla/mux"
)

func Register(w http.ResponseWriter, r *http.Request) {
	var req models.UserCreateRequest
	if err := response.BindJSON(r, &req); err != nil {
		response.RespondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}
	
	// Check if user already exists
	existingUser, _ := getUserByEmail(req.Email)
	if existingUser != nil {
		response.RespondWithError(w, http.StatusBadRequest, "Email already registered")
		return
	}
	
	// Create user
	user := &models.User{
		Email:     req.Email,
		FirstName: req.FirstName,
		LastName:  req.LastName,
		Phone:     req.Phone,
		Role:      req.Role,
		IsActive:  true,
	}
	
	if err := user.SetPassword(req.Password); err != nil {
		response.RespondWithError(w, http.StatusInternalServerError, "Could not create user")
		return
	}
	
	// Save user to database
	userID, err := createUser(user)
	if err != nil {
		response.RespondWithError(w, http.StatusInternalServerError, "Could not create user")
		return
	}
	user.ID = userID
	
	// Generate token
	token, err := utils.GenerateToken(user.ID, user.Email, string(user.Role))
	if err != nil {
		response.RespondWithError(w, http.StatusInternalServerError, "Could not generate token")
		return
	}
	
	response.RespondWithJSON(w, http.StatusCreated, models.AuthResponse{
		Token: token,
		User:  user,
	})
}

func Login(w http.ResponseWriter, r *http.Request) {
	var req models.LoginRequest
	if err := response.BindJSON(r, &req); err != nil {
		response.RespondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}
	
	user, err := getUserByEmail(req.Email)
	if err != nil {
		if err == sql.ErrNoRows {
			response.RespondWithError(w, http.StatusUnauthorized, "Invalid email or password")
			return
		}
		response.RespondWithError(w, http.StatusInternalServerError, "Database error")
		return
	}
	
	if !user.CheckPassword(req.Password) {
		response.RespondWithError(w, http.StatusUnauthorized, "Invalid email or password")
		return
	}
	
	if !user.IsActive {
		response.RespondWithError(w, http.StatusUnauthorized, "Account is deactivated")
		return
	}
	
	token, err := utils.GenerateToken(user.ID, user.Email, string(user.Role))
	if err != nil {
		response.RespondWithError(w, http.StatusInternalServerError, "Could not generate token")
		return
	}
	
	response.RespondWithJSON(w, http.StatusOK, models.AuthResponse{
		Token: token,
		User:  user,
	})
}

// Helper functions (to be implemented in repository)
func getUserByEmail(email string) (*models.User, error) {
	// Implementation would query the database
	return nil, sql.ErrNoRows
}

func createUser(user *models.User) (int64, error) {
	// Implementation would insert into database
	return 1, nil
}

internal/middleware/auth.go
go

package middleware

import (
	"context"
	"net/http"
	"strings"
	
	"ecommerce/internal/utils"
	"ecommerce/pkg/response"
)

type contextKey string

const UserContextKey = contextKey("user")

func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			response.RespondWithError(w, http.StatusUnauthorized, "Authorization header required")
			return
		}
		
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			response.RespondWithError(w, http.StatusUnauthorized, "Authorization header format must be Bearer {token}")
			return
		}
		
		claims, err := utils.VerifyToken(parts[1])
		if err != nil {
			response.RespondWithError(w, http.StatusUnauthorized, "Invalid token")
			return
		}
		
		// Add user info to context
		ctx := context.WithValue(r.Context(), UserContextKey, claims)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

🐳 Docker Configuration للنسخة Go
docker-compose.yml
yaml

version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/ecommerce?sslmode=disable
    depends_on:
      - db
    volumes:
      - .:/app
    command: ["./app"]

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ecommerce
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d

volumes:
  postgres_data:

Dockerfile
dockerfile

FROM golang:1.21-alpine

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o app ./cmd/server

EXPOSE 8080

CMD ["./app"]

📦 go.mod
go

module ecommerce

go 1.21

require (
	github.com/dgrijalva/jwt-go v3.2.0+incompatible
	github.com/gorilla/mux v1.8.0
	github.com/lib/pq v1.10.9
	golang.org/x/crypto v0.14.0
)
