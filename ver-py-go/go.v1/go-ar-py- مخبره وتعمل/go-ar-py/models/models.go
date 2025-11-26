package models

import (
	"time"

	"gorm.io/gorm"
)

// Product يمثل منتجًا في المتجر
type Product struct {
	ID          uint      `json:"id" gorm:"primaryKey"`
	Name        string    `json:"name" gorm:"not null;size:255"`
	Description string    `json:"description" gorm:"type:text"`
	Price       float64   `json:"price" gorm:"not null"`
	Stock       int       `json:"stock" gorm:"not null;default:0"`
	ImageURL    string    `json:"image_url" gorm:"size:500"`
	Category    string    `json:"category" gorm:"size:100"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `json:"-" gorm:"index"`
}

// User يمثل مستخدمًا في النظام
type User struct {
	ID        uint      `json:"id" gorm:"primaryKey"`
	FirstName string    `json:"first_name" gorm:"not null;size:100"`
	LastName  string    `json:"last_name" gorm:"not null;size:100"`
	Email     string    `json:"email" gorm:"uniqueIndex;not null;size:255"`
	Password  string    `json:"-" gorm:"not null;size:255"` // لا يتم إرجاع كلمة المرور في JSON
	Phone     string    `json:"phone" gorm:"size:20"`
	Address   string    `json:"address" gorm:"size:500"`
	Role      string    `json:"role" gorm:"default:'customer';size:50"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
}

// Order يمثل طلبًا في المتجر
type Order struct {
	ID         uint      `json:"id" gorm:"primaryKey"`
	UserID     uint      `json:"user_id" gorm:"not null;index"`
	User       User      `json:"user" gorm:"foreignKey:UserID"`
	Status     string    `json:"status" gorm:"default:'pending';size:50"` // pending, processing, shipped, delivered, cancelled
	Total      float64   `json:"total" gorm:"not null"`
	ShippingAddress string `json:"shipping_address" gorm:"not null;size:500"`
	PaymentMethod string `json:"payment_method" gorm:"not null;size:50"`
	PaymentStatus string `json:"payment_status" gorm:"default:'pending';size:50"` // pending, paid, failed, refunded
	OrderItems []OrderItem `json:"order_items" gorm:"foreignKey:OrderID"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
	DeletedAt  gorm.DeletedAt `json:"-" gorm:"index"`
}

// OrderItem يمثل عنصرًا في الطلب
type OrderItem struct {
	ID        uint    `json:"id" gorm:"primaryKey"`
	OrderID   uint    `json:"order_id" gorm:"not null;index"`
	Order     Order   `json:"order" gorm:"foreignKey:OrderID"`
	ProductID uint    `json:"product_id" gorm:"not null;index"`
	Product   Product `json:"product" gorm:"foreignKey:ProductID"`
	Quantity  int     `json:"quantity" gorm:"not null"`
	Price     float64 `json:"price" gorm:"not null"` // السعر عند وقت الشراء
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// Cart يمثل عربة تسوق المستخدم
type Cart struct {
	ID        uint        `json:"id" gorm:"primaryKey"`
	UserID    uint        `json:"user_id" gorm:"not null;uniqueIndex"`
	User      User        `json:"user" gorm:"foreignKey:UserID"`
	CartItems []CartItem  `json:"cart_items" gorm:"foreignKey:CartID"`
	CreatedAt time.Time   `json:"created_at"`
	UpdatedAt time.Time   `json:"updated_at"`
}

// CartItem يمثل عنصرًا في عربة التسوق
type CartItem struct {
	ID        uint    `json:"id" gorm:"primaryKey"`
	CartID    uint    `json:"cart_id" gorm:"not null;index"`
	Cart      Cart    `json:"cart" gorm:"foreignKey:CartID"`
	ProductID uint    `json:"product_id" gorm:"not null;index"`
	Product   Product `json:"product" gorm:"foreignKey:ProductID"`
	Quantity  int     `json:"quantity" gorm:"not null;default:1"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}
