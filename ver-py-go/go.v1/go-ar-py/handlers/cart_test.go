package handlers

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"go-ar-py/config"
	"go-ar-py/models"

	"github.com/go-chi/chi/v5"
	"github.com/golang-jwt/jwt/v4"
	"github.com/stretchr/testify/assert"
)

func TestCart(t *testing.T) {
	// Create a user and a product for testing
	db := config.GetDB()
	user := models.User{FirstName: "Test", LastName: "User", Email: "cart@example.com", Password: "password"}
	db.Create(&user)
	product := models.Product{Name: "Test Product", Price: 10.0, Stock: 100}
	db.Create(&product)

	// Get a token for the user
	token, _ := generateTestToken(user.ID)

	t.Run("it should get an empty cart for a new user", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/api/v1/cart", nil)
		req.Header.Set("Authorization", "Bearer "+token)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(GetCart)
		handler.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var cart models.Cart
		json.Unmarshal(rr.Body.Bytes(), &cart)
		assert.Empty(t, cart.CartItems)
	})

	t.Run("it should add a product to the cart", func(t *testing.T) {
		body := map[string]interface{}{
			"product_id": product.ID,
			"quantity":   1,
		}
		jsonBody, _ := json.Marshal(body)

		req, _ := http.NewRequest("POST", "/api/v1/cart", bytes.NewBuffer(jsonBody))
		req.Header.Set("Authorization", "Bearer "+token)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(AddToCart)
		handler.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var cart models.Cart
		json.Unmarshal(rr.Body.Bytes(), &cart)
		assert.Len(t, cart.CartItems, 1)
		assert.Equal(t, product.ID, cart.CartItems[0].ProductID)
	})

	t.Run("it should update the quantity of a product in the cart", func(t *testing.T) {
		// First, get the cart item to update
		var cart models.Cart
		db.Preload("CartItems").Where("user_id = ?", user.ID).First(&cart)
		cartItem := cart.CartItems[0]

		body := map[string]interface{}{
			"quantity": 2,
		}
		jsonBody, _ := json.Marshal(body)

		req, _ := http.NewRequest("PUT", fmt.Sprintf("/api/v1/cart?id=%d", cartItem.ID), bytes.NewBuffer(jsonBody))
		req.Header.Set("Authorization", "Bearer "+token)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Put("/api/v1/cart", UpdateCartItem)
		r.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var updatedCart models.Cart
		json.Unmarshal(rr.Body.Bytes(), &updatedCart)
		assert.Equal(t, 2, updatedCart.CartItems[0].Quantity)
	})

	t.Run("it should remove a product from the cart", func(t *testing.T) {
		// First, get the cart item to remove
		var cart models.Cart
		db.Preload("CartItems").Where("user_id = ?", user.ID).First(&cart)
		cartItem := cart.CartItems[0]

		req, _ := http.NewRequest("DELETE", fmt.Sprintf("/api/v1/cart?id=%d", cartItem.ID), nil)
		req.Header.Set("Authorization", "Bearer "+token)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Delete("/api/v1/cart", RemoveFromCart)
		r.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var updatedCart models.Cart
		json.Unmarshal(rr.Body.Bytes(), &updatedCart)
		assert.Empty(t, updatedCart.CartItems)
	})

	t.Run("it should clear the cart", func(t *testing.T) {
		// Add a product to the cart again
		body := map[string]interface{}{
			"product_id": product.ID,
			"quantity":   1,
		}
		jsonBody, _ := json.Marshal(body)
		addReq, _ := http.NewRequest("POST", "/api/v1/cart", bytes.NewBuffer(jsonBody))
		addReq.Header.Set("Authorization", "Bearer "+token)
		ctx := context.WithValue(addReq.Context(), "user_id", user.ID)
		addReq = addReq.WithContext(ctx)
		AddToCart(httptest.NewRecorder(), addReq)

		req, _ := http.NewRequest("DELETE", "/api/v1/cart/clear", nil)
		req.Header.Set("Authorization", "Bearer "+token)
		ctx = context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ClearCart)
		handler.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var cart models.Cart
		json.Unmarshal(rr.Body.Bytes(), &cart)
		assert.Empty(t, cart.CartItems)
	})

	// Clean up the database
	db.Exec("DELETE FROM users")
	db.Exec("DELETE FROM products")
	db.Exec("DELETE FROM carts")
	db.Exec("DELETE FROM cart_items")
}

func generateTestToken(userID uint) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id": userID,
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	})

	return token.SignedString([]byte(getSecretKey()))
}