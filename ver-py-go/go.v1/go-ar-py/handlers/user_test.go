package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"go-ar-py/config"
	"go-ar-py/models"

	"github.com/stretchr/testify/assert"
	"golang.org/x/crypto/bcrypt"
)

func TestRegisterUser(t *testing.T) {
	t.Run("it should register a new user with valid data", func(t *testing.T) {
		// Create the request body
		body := map[string]interface{}{
			"first_name": "Test",
			"last_name":  "User",
			"email":      "test@example.com",
			"password":   "password",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/users/register", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(RegisterUser)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusCreated, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var user models.User
		err = json.Unmarshal(rr.Body.Bytes(), &user)
		assert.NoError(t, err)
		assert.Equal(t, "Test", user.FirstName)
		assert.Equal(t, "User", user.LastName)
		assert.Equal(t, "test@example.com", user.Email)

		// Clean up the database
		db := config.GetDB()
		db.Exec("DELETE FROM users")
		db.Exec("DELETE FROM carts")
	})

	t.Run("it should return a conflict error if the user already exists", func(t *testing.T) {
		// Create a user in the test database
		db := config.GetDB()
		db.Create(&models.User{FirstName: "Test", LastName: "User", Email: "test@example.com", Password: "password"})

		// Create the request body
		body := map[string]interface{}{
			"first_name": "Test",
			"last_name":  "User",
			"email":      "test@example.com",
			"password":   "password",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/users/register", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(RegisterUser)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusConflict, rr.Code, "handler returned wrong status code")

		// Clean up the database
		db.Exec("DELETE FROM users")
	})
}

func TestLoginUser(t *testing.T) {
	t.Run("it should login a user with valid credentials", func(t *testing.T) {
		// Create a user in the test database
		db := config.GetDB()
		hashedPassword, _ := bcrypt.GenerateFromPassword([]byte("password"), bcrypt.DefaultCost)
		db.Create(&models.User{FirstName: "Test", LastName: "User", Email: "test@example.com", Password: string(hashedPassword)})

		// Create the request body
		body := map[string]interface{}{
			"email":    "test@example.com",
			"password": "password",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/users/login", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(LoginUser)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusOK, rr.Code, "handler returned wrong status code")

		// Check the response body is what we expect.
		var response map[string]interface{}
		err = json.Unmarshal(rr.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "token")

		// Clean up the database
		db.Exec("DELETE FROM users")
	})

	t.Run("it should return an unauthorized error with invalid credentials", func(t *testing.T) {
		// Create the request body
		body := map[string]interface{}{
			"email":    "test@example.com",
			"password": "wrongpassword",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a request to pass to our handler.
		req, err := http.NewRequest("POST", "/api/v1/users/login", bytes.NewBuffer(jsonBody))
		if err != nil {
			t.Fatal(err)
		}

		// We create a ResponseRecorder (which satisfies http.ResponseWriter) to record the response.
		rr := httptest.NewRecorder()
		handler := http.HandlerFunc(LoginUser)

		// Our handlers satisfy http.Handler, so we can call their ServeHTTP method
		// directly and pass in our Request and ResponseRecorder.
		handler.ServeHTTP(rr, req)

		// Check the status code is what we expect.
		assert.Equal(t, http.StatusUnauthorized, rr.Code, "handler returned wrong status code")
	})
}
