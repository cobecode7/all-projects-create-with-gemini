package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"go-ar-py/config"
	"go-ar-py/models"

	"github.com/go-chi/chi/v5"
)

// CreateOrderRequest هيكل طلب إنشاء طلب جديد
type CreateOrderRequest struct {
	Items           []OrderItemRequest `json:"items" binding:"required"`
	ShippingAddress string             `json:"shipping_address" binding:"required"`
	PaymentMethod   string             `json:"payment_method" binding:"required"`
}

// OrderItemRequest هيكل عنصر الطلب
type OrderItemRequest struct {
	ProductID uint `json:"product_id" binding:"required"`
	Quantity  int  `json:"quantity" binding:"required,min=1"`
}

// ListOrders يعرض قائمة الطلبات
func ListOrders(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		log.Printf("Error getting user ID from token: %v", err)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db := config.GetDB()
	var orders []models.Order

	// الحصول على معلمات التصفح
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page <= 0 {
		page = 1
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit <= 0 {
		limit = 10
	}

	// بناء الاستعلام - المستخدم العادي يرى طلباته فقط، والمشرف يرى كل الطلبات
	query := db.Model(&models.Order{}).Preload("OrderItems.Product")

	// التحقق من دور المستخدم
	var user models.User
	if err := db.First(&user, userID).Error; err != nil {
		log.Printf("Error fetching user: %v", err)
	}
	if user.Role != "admin" {
		query = query.Where("user_id = ?", userID)
	}

	// تنفيذ الاستعلام مع التصفح
	var total int64
	query.Count(&total)
	offset := (page - 1) * limit
	if err := query.Offset(offset).Limit(limit).Find(&orders).Error; err != nil {
		log.Printf("Error fetching orders: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// إعداد الاستجابة
	response := map[string]interface{}{
		"orders": orders,
		"total":  total,
		"page":   page,
		"limit":  limit,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// CreateOrder ينشئ طلبًا جديدًا
func CreateOrder(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		log.Printf("Error getting user ID from token: %v", err)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	var req CreateOrderRequest
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// التحقق من صحة البيانات
	if len(req.Items) == 0 {
		http.Error(w, "Order must contain at least one item", http.StatusBadRequest)
		return
	}

	// التحقق من وجود المنتجات وتوفرها
	var total float64
	var orderItems []models.OrderItem

	for _, item := range req.Items {
		var product models.Product
		if err := db.First(&product, item.ProductID).Error; err != nil {
			log.Printf("Product not found: %v", err)
			http.Error(w, "Product not found", http.StatusBadRequest)
			return
		}

		if product.Stock < item.Quantity {
			http.Error(w, "Insufficient stock for product: "+product.Name, http.StatusBadRequest)
			return
		}

		// حساب السعر الإجمالي
		itemTotal := product.Price * float64(item.Quantity)
		total += itemTotal

		// إضافة العنصر إلى قائمة عناصر الطلب
		orderItems = append(orderItems, models.OrderItem{
			ProductID: item.ProductID,
			Quantity:  item.Quantity,
			Price:     product.Price, // حفظ السعر عند وقت الشراء
		})

		// تحديث المخزون
		if err := db.Model(&product).Update("stock", product.Stock-item.Quantity).Error; err != nil {
			log.Printf("Error updating product stock: %v", err)
			return
		}
	}

	// إنشاء الطلب
	order := models.Order{
		UserID:          userID,
		Status:          "pending",
		Total:           total,
		ShippingAddress: req.ShippingAddress,
		PaymentMethod:   req.PaymentMethod,
		PaymentStatus:   "pending",
	}

	// بدء معاملة
	tx := db.Begin()

	// إنشاء الطلب
	if err := tx.Create(&order).Error; err != nil {
		log.Printf("Error creating order: %v", err)
		tx.Rollback()
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// إضافة عناصر الطلب
	for i := range orderItems {
		orderItems[i].OrderID = order.ID
		if err := tx.Create(&orderItems[i]).Error; err != nil {
			log.Printf("Error creating order item: %v", err)
			tx.Rollback()
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}

	// إتمام المعاملة
	tx.Commit()

	// إرجاع الطلب مع عناصره
	if err := db.Preload("OrderItems.Product").First(&order, order.ID).Error; err != nil {
		log.Printf("Error fetching order with items: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(order)
}

// GetOrder يعرض طلبًا محددًا
func GetOrder(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المستخدم
	userID, err := getUserIDFromToken(r)
	if err != nil {
		log.Printf("Error getting user ID from token: %v", err)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	orderID := chi.URLParam(r, "id")
	db := config.GetDB()

	var order models.Order
	if err := db.Preload("OrderItems.Product").First(&order, orderID).Error; err != nil {
		log.Printf("Order not found: %v", err)
		http.Error(w, "Order not found", http.StatusNotFound)
		return
	}

	// التحقق من أن المستخدم لديه صلاحية لعرض هذا الطلب
	var user models.User
	if err := db.First(&user, userID).Error; err != nil {
		log.Printf("Error fetching user: %v", err)
	}
	if user.Role != "admin" && order.UserID != userID {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(order)
}

// UpdateOrderStatus يحدث حالة الطلب (للمشرفين فقط)
func UpdateOrderStatus(w http.ResponseWriter, r *http.Request) {
	// التحقق من صلاحيات المشرف
	userID, err := getUserIDFromToken(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db := config.GetDB()
	var user models.User
	if err := db.First(&user, userID).Error; err != nil {
		log.Printf("Error fetching user: %v", err)
	}
	if user.Role != "admin" {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	orderID := chi.URLParam(r, "id")

	// فك تشفير جسم الطلب
	var req struct {
		Status string `json:"status" binding:"required"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// التحقق من صحة الحالة
	validStatuses := []string{"pending", "processing", "shipped", "delivered", "cancelled"}
	isValid := false
	for _, status := range validStatuses {
		if status == req.Status {
			isValid = true
			break
		}
	}
	if !isValid {
		http.Error(w, "Invalid status", http.StatusBadRequest)
		return
	}

	// تحديث حالة الطلب
	var order models.Order
	if err := db.First(&order, orderID).Error; err != nil {
		log.Printf("Order not found: %v", err)
		http.Error(w, "Order not found", http.StatusNotFound)
		return
	}

	if err := db.Model(&order).Update("status", req.Status).Error; err != nil {
		log.Printf("Error updating order status: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// إرجاع الطلب المحدث
	if err := db.First(&order, orderID).Error; err != nil {
		log.Printf("Error fetching updated order: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(order)
}
