package config

import (
	"log"
	"go-ar-py/models"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

// InitDatabase يهيئ الاتصال بقاعدة البيانات
func InitDatabase() {
	// استخدام قاعدة بيانات SQLite للتطوير

	// محاولة الاتصال بقاعدة البيانات
	var err error
	DB, err = gorm.Open(sqlite.Open("ecommerce.db"), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	log.Println("Database connection established")

	// ترحيل قاعدة البيانات
	err = DB.AutoMigrate(
		&models.Product{},
		&models.User{},
		&models.Order{},
		&models.OrderItem{},
		&models.Cart{},
		&models.CartItem{},
	)
	if err != nil {
		log.Fatalf("Failed to migrate database: %v", err)
	}

	log.Println("Database migration completed")
}

// GetDB يرجع مثيل قاعدة البيانات
func GetDB() *gorm.DB {
	return DB
}

// InitTestDatabase يهيئ قاعدة بيانات اختبارية في الذاكرة
func InitTestDatabase() {
	var err error
	DB, err = gorm.Open(sqlite.Open("file::memory:"), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		log.Fatalf("Failed to connect to test database: %v", err)
	}

	log.Println("Test database connection established")

	// ترحيل قاعدة البيانات
	err = DB.AutoMigrate(
		&models.Product{},
		&models.User{},
		&models.Order{},
		&models.OrderItem{},
		&models.Cart{},
		&models.CartItem{},
	)
	if err != nil {
		log.Fatalf("Failed to migrate test database: %v", err)
	}

	log.Println("Test database migration completed")
}
