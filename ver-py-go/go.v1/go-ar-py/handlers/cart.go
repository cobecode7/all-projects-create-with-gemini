package handlers

import (
	"encoding/json"
	"log"
	"net/http"

	"go-ar-py/config"
	"go-ar-py/models"
)

// GetCart يعرض محتويات عربة التسوق للمستخدم الحالي
func GetCart(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db := config.GetDB()

	// الحصول على عربة التسوق الخاصة بالمستخدم
	var cart models.Cart
	if err := db.Preload("CartItems.Product").Preload("User").Where("user_id = ?", userID).First(&cart).Error; err != nil {
		// إذا لم تكن عربة التسوق موجودة، قم بإنشائها
		cart = models.Cart{UserID: userID}
		if err := db.Create(&cart).Error; err != nil {
			log.Printf("Error creating cart: %v", err)
			http.Error(w, "Failed to create cart", http.StatusInternalServerError)
			return
		}
		// إعادة تحميل بيانات المستخدم بعد الإنشاء
		if err := db.Preload("User").First(&cart, cart.ID).Error; err != nil {
			log.Printf("Error loading cart user data: %v", err)
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(cart)
}

// AddToCartRequest هيكل طلب إضافة منتج إلى عربة التسوق
type AddToCartRequest struct {
	ProductID uint `json:"product_id" binding:"required"`
	Quantity  int  `json:"quantity" binding:"required,min=1"`
}

// AddToCart يضيف منتجًا إلى عربة التسوق
func AddToCart(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	var req AddToCartRequest
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// التحقق من وجود المنتج
	var product models.Product
	if err := db.First(&product, req.ProductID).Error; err != nil {
		http.Error(w, "Product not found", http.StatusBadRequest)
		return
	}

	// التحقق من توفر المنتج
	if product.Stock < req.Quantity {
		http.Error(w, "Insufficient stock", http.StatusBadRequest)
		return
	}

	// الحصول على عربة التسوق الخاصة بالمستخدم
	var cart models.Cart
	if err := db.Where("user_id = ?", userID).First(&cart).Error; err != nil {
		// إذا لم تكن عربة التسوق موجودة، قم بإنشائها
		cart = models.Cart{UserID: userID}
		if err := db.Create(&cart).Error; err != nil {
			log.Printf("Error creating cart: %v", err)
			http.Error(w, "Failed to create cart", http.StatusInternalServerError)
			return
		}
	}

	// التحقق مما إذا كان المنتج موجودًا بالفعل في عربة التسوق
	var cartItem models.CartItem
	if err := db.Where("cart_id = ? AND product_id = ?", cart.ID, req.ProductID).First(&cartItem).Error; err == nil {
		// تحديث الكمية إذا كان المنتج موجودًا بالفعل
		newQuantity := cartItem.Quantity + req.Quantity
		if product.Stock < newQuantity {
			http.Error(w, "Insufficient stock", http.StatusBadRequest)
			return
		}
		if err := db.Model(&cartItem).Update("quantity", newQuantity).Error; err != nil {
			log.Printf("Error updating cart item quantity: %v", err)
			http.Error(w, "Failed to update cart item", http.StatusInternalServerError)
			return
		}
	} else {
		// إضافة منتج جديد إلى عربة التسوق
		cartItem = models.CartItem{
			CartID:    cart.ID,
			ProductID: req.ProductID,
			Quantity:  req.Quantity,
		}
		if err := db.Create(&cartItem).Error; err != nil {
			log.Printf("Error creating cart item: %v", err)
			http.Error(w, "Failed to add item to cart", http.StatusInternalServerError)
			return
		}
	}

	// إرجاع عربة التسوق المحدثة
	if err := db.Preload("CartItems.Product").Preload("User").First(&cart, cart.ID).Error; err != nil {
		log.Printf("Error loading updated cart: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(cart)
}

// UpdateCartItemRequest هيكل طلب تحديث كمية منتج في عربة التسوق
type UpdateCartItemRequest struct {
	Quantity int `json:"quantity" binding:"required,min=1"`
}

// UpdateCartItem يحدث كمية منتج في عربة التسوق
func UpdateCartItem(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	cartItemID := r.URL.Query().Get("id")
	if cartItemID == "" {
		http.Error(w, "Cart item ID is required", http.StatusBadRequest)
		return
	}

	var req UpdateCartItemRequest
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// الحصول على عنصر عربة التسوق
	var cartItem models.CartItem
	if err := db.Preload("Cart").Preload("Product").First(&cartItem, cartItemID).Error; err != nil {
		http.Error(w, "Cart item not found", http.StatusNotFound)
		return
	}

	// التحقق من أن المستخدم هو صاحب عربة التسوق
	if cartItem.Cart.UserID != userID {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// التحقق من توفر المنتج
	if cartItem.Product.Stock < req.Quantity {
		http.Error(w, "Insufficient stock", http.StatusBadRequest)
		return
	}

	// تحديث الكمية
	if err := db.Model(&cartItem).Update("quantity", req.Quantity).Error; err != nil {
		log.Printf("Error updating cart item quantity: %v", err)
		http.Error(w, "Failed to update cart item", http.StatusInternalServerError)
		return
	}

	// إرجاع عربة التسوق المحدثة
	var cart models.Cart
	if err := db.Preload("CartItems.Product").Preload("User").First(&cart, cartItem.CartID).Error; err != nil {
		log.Printf("Error loading updated cart: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(cart)
}

// RemoveFromCart يزيل منتجًا من عربة التسوق
func RemoveFromCart(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	cartItemID := r.URL.Query().Get("id")
	if cartItemID == "" {
		http.Error(w, "Cart item ID is required", http.StatusBadRequest)
		return
	}

	db := config.GetDB()

	// الحصول على عنصر عربة التسوق
	var cartItem models.CartItem
	if err := db.Preload("Cart").First(&cartItem, cartItemID).Error; err != nil {
		http.Error(w, "Cart item not found", http.StatusNotFound)
		return
	}

	// التحقق من أن المستخدم هو صاحب عربة التسوق
	if cartItem.Cart.UserID != userID {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// حذف العنصر
	if err := db.Delete(&cartItem).Error; err != nil {
		log.Printf("Error deleting cart item: %v", err)
		http.Error(w, "Failed to remove item from cart", http.StatusInternalServerError)
		return
	}

	// إرجاع عربة التسوق المحدثة
	var cart models.Cart
	if err := db.Preload("CartItems.Product").Preload("User").First(&cart, cartItem.CartID).Error; err != nil {
		log.Printf("Error loading updated cart: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(cart)
}

// ClearCart يفرغ محتويات عربة التسوق
func ClearCart(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db := config.GetDB()

	// الحصول على عربة التسوق الخاصة بالمستخدم
	var cart models.Cart
	if err := db.Where("user_id = ?", userID).First(&cart).Error; err != nil {
		http.Error(w, "Cart not found", http.StatusNotFound)
		return
	}

	// حذف جميع عناصر عربة التسوق
	if err := db.Where("cart_id = ?", cart.ID).Delete(&models.CartItem{}).Error; err != nil {
		log.Printf("Error clearing cart items: %v", err)
		http.Error(w, "Failed to clear cart", http.StatusInternalServerError)
		return
	}

	// إرجاع عربة التسوق الفارغة
	if err := db.Preload("CartItems.Product").First(&cart, cart.ID).Error; err != nil {
		log.Printf("Error loading cleared cart: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(cart)
}
