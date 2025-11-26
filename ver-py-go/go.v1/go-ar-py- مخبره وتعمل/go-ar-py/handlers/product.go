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

// ListProducts يعرض قائمة المنتجات
func ListProducts(w http.ResponseWriter, r *http.Request) {
	var products []models.Product
	db := config.GetDB()

	// الحصول على معلمات التصفح والبحث
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page <= 0 {
		page = 1
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit <= 0 {
		limit = 10
	}
	category := r.URL.Query().Get("category")
	search := r.URL.Query().Get("search")

	// بناء الاستعلام
	query := db.Model(&models.Product{})
	if category != "" {
		query = query.Where("category = ?", category)
	}
	if search != "" {
		// تحقق من نوع قاعدة البيانات
		dialector := db.Dialector.Name()
		if dialector == "postgres" {
			// PostgreSQL يدعم ILIKE للبحث غير الحساس لحالة الأحرف
			query = query.Where("name ILIKE ? OR description ILIKE ?", "%"+search+"%", "%"+search+"%")
		} else {
			// SQLite وغيرها لا تدعم ILIKE، نستخدم LIKE
			query = query.Where("name LIKE ? OR description LIKE ?", "%"+search+"%", "%"+search+"%")
		}
	}

	// تنفيذ الاستعلام مع التصفح
	var total int64
	query.Count(&total)
	offset := (page - 1) * limit
	if err := query.Offset(offset).Limit(limit).Find(&products).Error; err != nil {
		log.Printf("Error fetching products: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// إعداد الاستجابة
	response := map[string]interface{}{
		"products": products,
		"total":    total,
		"page":     page,
		"limit":    limit,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// CreateProduct ينشئ منتجًا جديدًا
func CreateProduct(w http.ResponseWriter, r *http.Request) {
	var product models.Product
	db := config.GetDB()

	// فك تشفير جسم الطلب
	if err := json.NewDecoder(r.Body).Decode(&product); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// التحقق من صحة البيانات
	if product.Name == "" || product.Price <= 0 || product.Stock < 0 {
		http.Error(w, "Invalid product data", http.StatusBadRequest)
		return
	}

	// إنشاء المنتج
	if err := db.Create(&product).Error; err != nil {
		log.Printf("Error creating product: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(product)
}

// GetProduct يعرض منتجًا محددًا
func GetProduct(w http.ResponseWriter, r *http.Request) {
	productID := chi.URLParam(r, "id")
	db := config.GetDB()

	var product models.Product
	if err := db.First(&product, productID).Error; err != nil {
		log.Printf("Error fetching product: %v", err)
		http.Error(w, "Product not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(product)
}

// UpdateProduct يحدث منتجًا محددًا
func UpdateProduct(w http.ResponseWriter, r *http.Request) {
	productID := chi.URLParam(r, "id")
	db := config.GetDB()

	// التحقق من وجود المنتج
	var product models.Product
	if err := db.First(&product, productID).Error; err != nil {
		log.Printf("Error fetching product: %v", err)
		http.Error(w, "Product not found", http.StatusNotFound)
		return
	}

	// فك تشفير جسم الطلب
	var updateData models.Product
	if err := json.NewDecoder(r.Body).Decode(&updateData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// تحديث المنتج
	if err := db.Model(&product).Updates(updateData).Error; err != nil {
		log.Printf("Error updating product: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// الحصول على المنتج المحدث
	if err := db.First(&product, productID).Error; err != nil {
		log.Printf("Error fetching updated product: %v", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(product)
}

// DeleteProduct يحذف منتجًا محددًا
func DeleteProduct(w http.ResponseWriter, r *http.Request) {
	productID := chi.URLParam(r, "id")
	db := config.GetDB()

	// التحقق من وجود المنتج
	var product models.Product
	if err := db.First(&product, productID).Error; err != nil {
		log.Printf("Error fetching product: %v", err)
		http.Error(w, "Product not found", http.StatusNotFound)
		return
	}

	// حذف المنتج
	if err := db.Delete(&product).Error; err != nil {
		log.Printf("Error deleting product: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{"message": "Product deleted successfully"})
}
