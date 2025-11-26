package middleware

import (
	"context"
	"net/http"
	"strings"
	"os"

	"github.com/golang-jwt/jwt/v4"
)

// AuthMiddleware يتحقق من صحة التوكن
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		tokenString := extractTokenFromRequest(r)
		if tokenString == "" {
			http.Error(w, "Authorization token required", http.StatusUnauthorized)
			return
		}

		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, jwt.ErrSignatureInvalid
			}
			return []byte(getSecretKey()), nil
		})

		if err != nil {
			http.Error(w, "Invalid token", http.StatusUnauthorized)
			return
		}

		if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
			// إضافة معلومات المستخدم إلى السياق
			ctx := context.WithValue(r.Context(), "user_id", uint(claims["user_id"].(float64)))
			ctx = context.WithValue(ctx, "email", claims["email"].(string))
			ctx = context.WithValue(ctx, "role", claims["role"].(string))

			next.ServeHTTP(w, r.WithContext(ctx))
		} else {
			http.Error(w, "Invalid token", http.StatusUnauthorized)
		}
	})
}

// AdminMiddleware يتحقق من أن المستخدم لديه صلاحيات المشرف
func AdminMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		role, ok := r.Context().Value("role").(string)
		if !ok || role != "admin" {
			http.Error(w, "Admin access required", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// دالة مساعدة لاستخراج التوكن من الطلب
func extractTokenFromRequest(r *http.Request) string {
	bearerToken := r.Header.Get("Authorization")
	if len(strings.Split(bearerToken, " ")) == 2 {
		return strings.Split(bearerToken, " ")[1]
	}
	return ""
}

// دالة مساعدة للحصول على مفتاح التوقيع
func getSecretKey() string {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		// قيمة افتراضية للتطوير فقط - يجب تغييرها في الإنتاج
		secret = "default-secret-key-change-in-production"
	}
	return secret
}

// دالة مساعدة للحصول على معرف المستخدم من السياق
func GetUserIDFromContext(ctx context.Context) (uint, bool) {
	userID, ok := ctx.Value("user_id").(uint)
	return userID, ok
}

// دالة مساعدة للحصول على دور المستخدم من السياق
func GetUserRoleFromContext(ctx context.Context) (string, bool) {
	role, ok := ctx.Value("role").(string)
	return role, ok
}
