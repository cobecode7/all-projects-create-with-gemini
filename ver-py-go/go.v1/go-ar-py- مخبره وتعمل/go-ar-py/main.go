package main

import (
	"log"
	"net/http"
	"os"

	"go-ar-py/config"
	"go-ar-py/handlers"
	authMiddleware "go-ar-py/middleware"

	"github.com/go-chi/chi/v5"
	chiMiddleware "github.com/go-chi/chi/v5/middleware"
	"github.com/joho/godotenv"
)

func main() {
	// تحميل متغيرات البيئة من ملف .env
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found")
	}

	// تهيئة قاعدة البيانات
	config.InitDatabase()

	// إنشاء موجه التوجيه
	r := chi.NewRouter()

	// إضافة الوسيطة
	r.Use(chiMiddleware.Logger)
	r.Use(chiMiddleware.Recoverer)
	r.Use(chiMiddleware.RequestID)
	r.Use(chiMiddleware.RealIP)
	r.Use(chiMiddleware.AllowContentType("application/json"))

	// إضافة مسارات API
	setupRoutes(r)

	// بدء الخادم
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Starting server on port %s", port)
	if err := http.ListenAndServe(":"+port, r); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func setupRoutes(r *chi.Mux) {
	// مسارات المنتجات (متاحة للجميع)
	r.Route("/api/v1/products", func(r chi.Router) {
		r.Get("/", handlers.ListProducts)
		r.Get("/{id}", handlers.GetProduct)

		// مسارات تتطلب المصادقة
		r.Group(func(r chi.Router) {
			r.Use(authMiddleware.AuthMiddleware)

			// مسارات إنشاء وتحديث وحذف المنتجات تتطلب صلاحيات المشرف
			r.Group(func(r chi.Router) {
				r.Use(authMiddleware.AdminMiddleware)
				r.Post("/", handlers.CreateProduct)
				r.Put("/{id}", handlers.UpdateProduct)
				r.Delete("/{id}", handlers.DeleteProduct)
			})
		})
	})

	// مسارات المستخدمين
	r.Route("/api/v1/users", func(r chi.Router) {
		r.Post("/register", handlers.RegisterUser)
		r.Post("/login", handlers.LoginUser)

		// مسارات تتطلب المصادقة
		r.Group(func(r chi.Router) {
			r.Use(authMiddleware.AuthMiddleware)
			r.Get("/profile", handlers.GetUserProfile)
		})
	})

	// مسارات عربة التسوق (تتطلب المصادقة)
	r.Route("/api/v1/cart", func(r chi.Router) {
		r.Use(authMiddleware.AuthMiddleware)
		r.Get("/", handlers.GetCart)
		r.Post("/", handlers.AddToCart)
		r.Put("/", handlers.UpdateCartItem)
		r.Delete("/", handlers.RemoveFromCart)
		r.Delete("/clear", handlers.ClearCart)
	})

	// مسارات الطلبات (تتطلب المصادقة)
	r.Route("/api/v1/orders", func(r chi.Router) {
		r.Use(authMiddleware.AuthMiddleware)
		r.Get("/", handlers.ListOrders)
		r.Post("/", handlers.CreateOrder)
		r.Get("/{id}", handlers.GetOrder)

		// مسارات تحديث حالة الطلب تتطلب صلاحيات المشرف
		r.Group(func(r chi.Router) {
			r.Use(authMiddleware.AdminMiddleware)
			r.Put("/{id}/status", handlers.UpdateOrderStatus)
		})
	})
}
