package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"go-ar-py/config"
	"go-ar-py/models"

	"golang.org/x/crypto/bcrypt"
	"github.com/golang-jwt/jwt/v4"
)

// RegisterRequest هيكل طلب تسجيل المستخدم
type RegisterRequest struct {
	FirstName string `json:"first_name" binding:"required"`
	LastName  string `json:"last_name" binding:"required"`
	Email     string `json:"email" binding:"required,email"`
	Password  string `json:"password" binding:"required,min=6"`
	Phone     string `json:"phone"`
	Address   string `json:"address"`
	Role      string `json:"role"`
}

// LoginRequest هيكل طلب تسجيل الدخول
type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

// RegisterUser يسجل مستخدمًا جديدًا
func RegisterUser(w http.ResponseWriter, r *http.Request) {
	var req RegisterRequest
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// التحقق من وجود المستخدم مسبقًا
	var existingUser models.User
	if err := db.Where("email = ?", req.Email).First(&existingUser).Error; err == nil {
		log.Printf("User with email %s already exists", req.Email)
		http.Error(w, "User with this email already exists", http.StatusConflict)
		return
	}

	// تشفير كلمة المرور
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		log.Printf("Error hashing password: %v", err)
		http.Error(w, "Failed to hash password", http.StatusInternalServerError)
		return
	}

	// تحديد الدور
	role := "customer" // الدور الافتراضي
	if req.Role != "" {
		role = req.Role
	}

	// إنشاء المستخدم الجديد
	user := models.User{
		FirstName: req.FirstName,
		LastName:  req.LastName,
		Email:     req.Email,
		Password:  string(hashedPassword),
		Phone:     req.Phone,
		Address:   req.Address,
		Role:      role,
	}

	if err := db.Create(&user).Error; err != nil {
		log.Printf("Error creating user: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// إنشاء عربة تسوق للمستخدم
	cart := models.Cart{UserID: user.ID}
	if err := db.Create(&cart).Error; err != nil {
		log.Printf("Error creating cart for user %d: %v", user.ID, err)
	}

	// إزالة كلمة المرور من الاستجابة
	user.Password = ""

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

// LoginUser يقوم بتسجيل دخول المستخدم
func LoginUser(w http.ResponseWriter, r *http.Request) {
	var req LoginRequest
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// البحث عن المستخدم
	var user models.User
	if err := db.Where("email = ?", req.Email).First(&user).Error; err != nil {
		log.Printf("Login attempt with non-existent email: %s", req.Email)
		http.Error(w, "Invalid email or password", http.StatusUnauthorized)
		return
	}

	// التحقق من كلمة المرور
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		log.Printf("Invalid password attempt for email: %s", req.Email)
		http.Error(w, "Invalid email or password", http.StatusUnauthorized)
		return
	}

	// إنشاء JWT token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id": user.ID,
		"email":   user.Email,
		"role":    user.Role,
		"exp":     time.Now().Add(time.Hour * 24 * 7).Unix(), // صلاحية أسبوع واحد
	})

	// الحصول على مفتاح التوقيع من متغيرات البيئة
	secretKey := []byte(getSecretKey())
	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		log.Printf("Error generating JWT token: %v", err)
		http.Error(w, "Failed to generate token", http.StatusInternalServerError)
		return
	}

	// إزالة كلمة المرور من الاستجابة
	user.Password = ""

	// إعداد الاستجابة
	response := map[string]interface{}{
		"user":  user,
		"token": tokenString,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// GetUserProfile يعرض معلومات المستخدم الحالي
func GetUserProfile(w http.ResponseWriter, r *http.Request) {
	// الحصول على معلومات المستخدم من JWT token
	userID, err := getUserIDFromToken(r)
	if err != nil {
		log.Printf("Error getting user ID from token: %v", err)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db := config.GetDB()
	var user models.User
	if err := db.First(&user, userID).Error; err != nil {
		log.Printf("Error fetching user profile: %v", err)
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	// إزالة كلمة المرور من الاستجابة
	user.Password = ""

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(user)
}


