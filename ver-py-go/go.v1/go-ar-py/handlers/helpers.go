package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/golang-jwt/jwt/v4"
)

// getUserIDFromToken يستخرج معرف المستخدم من التوكن
func getUserIDFromToken(r *http.Request) (uint, error) {
	tokenString := extractTokenFromRequest(r)
	if tokenString == "" {
		return 0, fmt.Errorf("no token provided")
	}

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(getSecretKey()), nil
	})

	if err != nil {
		log.Printf("Error parsing JWT token: %v", err)
		return 0, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		userID := uint(claims["user_id"].(float64))
		return userID, nil
	}

	return 0, fmt.Errorf("invalid token")
}

// extractTokenFromRequest يستخرج التوكن من الطلب
func extractTokenFromRequest(r *http.Request) string {
	bearerToken := r.Header.Get("Authorization")
	if len(strings.Split(bearerToken, " ")) == 2 {
		return strings.Split(bearerToken, " ")[1]
	}
	return ""
}

// getSecretKey يحصل على مفتاح التوقيع
func getSecretKey() string {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		// قيمة افتراضية للتطوير فقط - يجب تغييرها في الإنتاج
		secret = "default-secret-key-change-in-production"
	}
	return secret
}
