package handlers

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"go-ar-py/config"
	"go-ar-py/models"

	"github.com/go-chi/chi/v5"
	"github.com/stretchr/testify/assert"
)

// TestMain is executed before any tests in this package
func TestMain(m *testing.M) {
	// Set up the test database
	config.InitTestDatabase()

	// Run the tests
	exitCode := m.Run()

	// Exit with the same code
	os.Exit(exitCode)
}

func TestListProducts(t *testing.T) {
	t.Run("it should return an empty list when there are no products", func(t *testing.T) {
		// Create a request to pass to our handler.
		req, err := http.NewRequest("GET", "/api/v1/products", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListProducts)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)

		products, ok := response["products"].([]interface{})
		assert.True(t, ok)
		assert.Len(t, products, 0)
	})

	t.Run("it should return a list of products", func(t *testing.T) {
		// Create some products in the test database
		db := config.GetDB()
		db.Create(&models.Product{Name: "Product 1", Price: 10.0, Stock: 100})
		db.Create(&models.Product{Name: "Product 2", Price: 20.0, Stock: 200})

		// Create a request to pass to our handler.
		req, err := http.NewRequest("GET", "/api/v1/products", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListProducts)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)

		products, ok := response["products"].([]interface{})
		assert.True(t, ok)
		assert.Len(t, products, 2)

		// Clean up the database
		db.Exec("DELETE FROM products")
	})

	t.Run("it should filter products by category", func(t *testing.T) {
		// Create some products in the test database
		db := config.GetDB()
		db.Create(&models.Product{Name: "Product 1", Price: 10.0, Stock: 100, Category: "electronics"})
		db.Create(&models.Product{Name: "Product 2", Price: 20.0, Stock: 200, Category: "clothing"})
		db.Create(&models.Product{Name: "Product 3", Price: 30.0, Stock: 300, Category: "electronics"})

		// Create a request to pass to our handler with category filter
		req, err := http.NewRequest("GET", "/api/v1/products?category=electronics", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListProducts)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)

		products, ok := response["products"].([]interface{})
		assert.True(t, ok)
		assert.Len(t, products, 2) // Should only return electronics products

		// Clean up the database
		db.Exec("DELETE FROM products")
	})

	t.Run("it should search products by name", func(t *testing.T) {
		// Create some products in the test database
		db := config.GetDB()
		db.Create(&models.Product{Name: "Laptop", Price: 1000.0, Stock: 10, Description: "A powerful laptop"})
		db.Create(&models.Product{Name: "Phone", Price: 500.0, Stock: 20, Description: "A smartphone"})
		db.Create(&models.Product{Name: "Desktop", Price: 800.0, Stock: 15, Description: "A desktop computer"})

		// Create a request to pass to our handler with search term
		req, err := http.NewRequest("GET", "/api/v1/products?search=computer", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListProducts)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Print the response body for debugging
		t.Logf("Response body: %s", rr.Body.String())

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)

		products, ok := response["products"].([]interface{})
		assert.True(t, ok)
		assert.Len(t, products, 1) // Should only return the desktop computer

		// Clean up the database
		db.Exec("DELETE FROM products")

		// Clean up the database
		db.Exec("DELETE FROM products")
	})

	t.Run("it should paginate results", func(t *testing.T) {
		// Create some products in the test database
		db := config.GetDB()
		for i := 1; i <= 15; i++ {
			db.Create(&models.Product{Name: fmt.Sprintf("Product %d", i), Price: float64(i * 10), Stock: i * 5})
		}

		// Create a request to pass to our handler with pagination
		req, err := http.NewRequest("GET", "/api/v1/products?page=2&limit=5", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(ListProducts)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)

		products, ok := response["products"].([]interface{})
		assert.True(t, ok)
		assert.Len(t, products, 5) // Should return 5 products for page 2

		// Check pagination info
		assert.Equal(t, float64(2), response["page"])
		assert.Equal(t, float64(5), response["limit"])
		assert.Equal(t, float64(15), response["total"])

		// Clean up the database
		db.Exec("DELETE FROM products")
	})
}

func TestCreateProduct(t *testing.T) {
	t.Run("it should create a new product with valid data", func(t *testing.T) {
		// Create the request body
		body := map[string]interface{}{
			"name":  "New Product",
			"price": 50.0,
			"stock": 100,
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/products", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(CreateProduct)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusCreated, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var product models.Product
		err = json.Unmarshal(rr.Body.Bytes(), &product)
		assert.NoError(t, err)
		assert.Equal(t, "New Product", product.Name)

		// Clean up the database
		db := config.GetDB()
		db.Exec("DELETE FROM products")
	})

	t.Run("it should return a bad request error for invalid data", func(t *testing.T) {
		// Create the request body with invalid data
		body := map[string]interface{}{
			"name": "", // Invalid name
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/products", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(CreateProduct)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusBadRequest, rr.Code, "handler returned wrong status code")
	})
}

func TestGetProduct(t *testing.T) {
	t.Run("it should return a product when it exists", func(t *testing.T) {
		// Create a product in the test database
		db := config.GetDB()
		product := models.Product{Name: "Test Product", Price: 10.0, Stock: 100}
		db.Create(&product)

		// Print the product ID for debugging
		t.Logf("Created product with ID: %d", product.ID)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("GET", fmt.Sprintf("/api/v1/products/%d", product.ID), nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Get("/api/v1/products/{id}", GetProduct)
		r.ServeHTTP(rr, req)


		// Print response body for debugging
		t.Logf("Response body: %s", rr.Body.String())

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var responseProduct models.Product
		err = json.Unmarshal(rr.Body.Bytes(), &responseProduct)
		assert.NoError(t, err)
		assert.Equal(t, "Test Product", responseProduct.Name)

		// Clean up the database
		db.Exec("DELETE FROM products")
	})

	t.Run("it should return a not found error when the product doesn't exist", func(t *testing.T) {
		// Create a request to pass to our handler.
		req, err := http.NewRequest("GET", "/api/v1/products/999", nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Get("/api/v1/products/{id}", GetProduct)
		r.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusNotFound, rr.Code, "handler returned wrong status code")
	})
}

func TestUpdateProduct(t *testing.T) {
	t.Run("it should update a product when it exists", func(t *testing.T) {
		// Create a product in the test database
		db := config.GetDB()
		product := models.Product{Name: "Test Product", Price: 10.0, Stock: 100}
		db.Create(&product)

		// Create the request body with updated data
		updateData := map[string]interface{}{
			"name":  "Updated Product",
			"price": 20.0,
			"stock": 200,
		}
		jsonBody, _ := json.Marshal(updateData)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("PUT", fmt.Sprintf("/api/v1/products/%d", product.ID), bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Put("/api/v1/products/{id}", UpdateProduct)
		r.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var responseProduct models.Product
		err = json.Unmarshal(rr.Body.Bytes(), &responseProduct)
		assert.NoError(t, err)
		assert.Equal(t, "Updated Product", responseProduct.Name)
		assert.Equal(t, 20.0, responseProduct.Price)
		assert.Equal(t, 200, responseProduct.Stock)

		// Clean up the database
		db.Exec("DELETE FROM products")
	})

	t.Run("it should return a not found error when the product doesn't exist", func(t *testing.T) {
		// Create the request body with updated data
		updateData := map[string]interface{}{
			"name":  "Updated Product",
			"price": 20.0,
			"stock": 200,
		}
		jsonBody, _ := json.Marshal(updateData)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("PUT", "/api/v1/products/999", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// Create a chi router context and set the URL parameter
		rctx := chi.NewRouteContext()
		rctx.URLParams.Add("id", "999")
		req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(UpdateProduct)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusNotFound, rr.Code, "handler returned wrong status code")
	})
}

func TestDeleteProduct(t *testing.T) {
	t.Run("it should delete a product when it exists", func(t *testing.T) {
		// Create a product in the test database
		db := config.GetDB()
		product := models.Product{Name: "Test Product", Price: 10.0, Stock: 100}
		db.Create(&product)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("DELETE", fmt.Sprintf("/api/v1/products/%d", product.ID), nil)
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		r := chi.NewRouter()
		r.Delete("/api/v1/products/{id}", DeleteProduct)
		r.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]string
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Equal(t, "Product deleted successfully", response["message"])

		// Verify the product is deleted
		var deletedProduct models.Product
		err = db.First(&deletedProduct, 1).Error
		assert.Error(t, err) // Should return an error because the product is deleted

		// Clean up the database (in case the soft delete didn't work)
		db.Exec("DELETE FROM products")
	})

	t.Run("it should return a not found error when the product doesn't exist", func(t *testing.T) {
		// Create a request to pass to our handler.
		req, err := http.NewRequest("DELETE", "/api/v1/products/999", nil)
		if err != nil {
			t.Fatal(err)
		}

		// Create a chi router context and set the URL parameter
		rctx := chi.NewRouteContext()
		rctx.URLParams.Add("id", "999")
		req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(DeleteProduct)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusNotFound, rr.Code, "handler returned wrong status code")
	})
}
