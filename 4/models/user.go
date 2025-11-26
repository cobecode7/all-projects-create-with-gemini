package models

import "gorm.io/gorm"

// User represents a user in the database

type User struct {
	gorm.Model
	Name     string `form:"name" json:"name"`
	Email    string `form:"email" json:"email" gorm:"unique"`
	Password string `form:"password" json:"-"`
}