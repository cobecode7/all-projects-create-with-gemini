package handlers

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"go-ar-py/config"
	"go-ar-py/models"

	"github.com/go-chi/chi/v5"
	"github.com/stretchr/testify/assert"
)

func TestOrder(t *testing.T) {
	// Create a user and a product for testing
	db := config.GetDB()
	user := models.User{FirstName: "Test", LastName: "User", Email: "order@example.com", Password: "password", Role: "customer"}
	db.Create(&user)
	admin := models.User{FirstName: "Admin", LastName: "User", Email: "admin@example.com", Password: "password", Role: "admin"}
	db.Create(&admin)
	product := models.Product{Name: "Test Product", Price: 10.0, Stock: 100}
	db.Create(&product)

	// Get a token for the user and admin
	userToken, _ := generateTestToken(user.ID)
	adminToken, _ := generateTestToken(admin.ID)

	t.Run("it should create an order", func(t *testing.T) {
		items := []OrderItemRequest{{
			ProductID: product.ID,
			Quantity:  1,
		}}
		body := CreateOrderRequest{
			Items:           items,
			ShippingAddress: "123 Test St",
			PaymentMethod:   "card",
		}
		jsonBody, _ := json.Marshal(body)

		req, _ := http.NewRequest("POST", "/api/v1/orders", bytes.NewBuffer(jsonBody))
		req.Header.Set("Authorization", "Bearer "+userToken)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(CreateOrder)
		handler.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusCreated, rr.Code)
		var order models.Order
		json.Unmarshal(rr.Body.Bytes(), &order)
		assert.Equal(t, user.ID, order.UserID)
		assert.Len(t, order.OrderItems, 1)
	})

	t.Run("it should list orders for a user", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/api/v1/orders", nil)
		req.Header.Set("Authorization", "Bearer "+userToken)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListOrders)
		handler.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var response map[string]interface{}
		json.Unmarshal(rr.Body.Bytes(), &response)
		orders, _ := response["orders"].([]interface{})
		assert.Len(t, orders, 1)
	})

	t.Run("it should get an order by id", func(t *testing.T) {
		var order models.Order
		db.Where("user_id = ?", user.ID).First(&order)

		req, _ := http.NewRequest("GET", fmt.Sprintf("/api/v1/orders/%d", order.ID), nil)
		req.Header.Set("Authorization", "Bearer "+userToken)
		ctx := context.WithValue(req.Context(), "user_id", user.ID)
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Get("/api/v1/orders/{id}", GetOrder)
		r.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var fetchedOrder models.Order
		json.Unmarshal(rr.Body.Bytes(), &fetchedOrder)
		assert.Equal(t, order.ID, fetchedOrder.ID)
	})

	t.Run("it should update order status as admin", func(t *testing.T) {
		var order models.Order
		db.Where("user_id = ?", user.ID).First(&order)

		body := map[string]interface{}{"status": "shipped"}
		jsonBody, _ := json.Marshal(body)

		req, _ := http.NewRequest("PUT", fmt.Sprintf("/api/v1/orders/%d/status", order.ID), bytes.NewBuffer(jsonBody))
		req.Header.Set("Authorization", "Bearer "+adminToken)
		ctx := context.WithValue(req.Context(), "user_id", admin.ID)
		ctx = context.WithValue(ctx, "role", "admin")
		req = req.WithContext(ctx)

		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Put("/api/v1/orders/{id}/status", UpdateOrderStatus)
		r.ServeHTTP(rr, req)

		assert.Equal(t, http.StatusOK, rr.Code)
		var updatedOrder models.Order
		json.Unmarshal(rr.Body.Bytes(), &updatedOrder)
		assert.Equal(t, "shipped", updatedOrder.Status)
	})

	// Clean up the database
	db.Exec("DELETE FROM users")
	db.Exec("DELETE FROM products")
	db.Exec("DELETE FROM orders")
	db.Exec("DELETE FROM order_items")
}
