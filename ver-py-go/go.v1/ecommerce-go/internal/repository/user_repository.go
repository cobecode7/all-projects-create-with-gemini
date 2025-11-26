package repository

import (
	"errors"

	"github.com/jmoiron/sqlx"
	"github.com/yourusername/ecommerce-go/internal/models"
)

type UserRepository struct {
	DB *sqlx.DB
}

func NewUserRepository(db *sqlx.DB) *UserRepository {
	return &UserRepository{DB: db}
}

func (r *UserRepository) Create(user *models.User) error {
	query := `INSERT INTO users (name, email, password, created_at, updated_at)
	          VALUES ($1, $2, $3, NOW(), NOW()) RETURNING id`
	err := r.DB.QueryRow(query, user.Name, user.Email, user.Password).Scan(&user.ID)
	if err != nil {
		return err
	}
	return nil
}

func (r *UserRepository) FindByEmail(email string) (*models.User, error) {
	var user models.User
	err := r.DB.Get(&user, "SELECT * FROM users WHERE email = $1", email)
	if err != nil {
		return nil, errors.New("user not found")
	}
	return &user, nil
}
