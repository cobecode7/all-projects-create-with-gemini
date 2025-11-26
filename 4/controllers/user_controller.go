package controllers

import (
	"net/http"

	"gemini-project/models"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/sessions"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

// UserController holds the database connection and session store

type UserController struct {
	DB    *gorm.DB
	Store sessions.Store
}

// NewUserController creates a new UserController
func NewUserController(db *gorm.DB, store sessions.Store) *UserController {
	return &UserController{DB: db, Store: store}
}

// ShowLogin renders the login page
func (ctrl *UserController) ShowLogin(c *gin.Context) {
	c.HTML(http.StatusOK, "base.html", gin.H{
		"title": "Login",
	})
}

// ShowRegister renders the register page
func (ctrl *UserController) ShowRegister(c *gin.Context) {
	c.HTML(http.StatusOK, "base.html", gin.H{
		"title": "Register",
	})
}

// RegisterUser handles user registration
func (ctrl *UserController) RegisterUser(c *gin.Context) {
	var user models.User
	if err := c.ShouldBind(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to hash password"})
		return
	}

	user.Password = string(hashedPassword)

	if err := ctrl.DB.Create(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create user"})
		return
	}

	c.Redirect(http.StatusFound, "/")
}

// LoginUser handles user login
func (ctrl *UserController) LoginUser(c *gin.Context) {
	var loginDetails models.User
	if err := c.ShouldBind(&loginDetails); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user models.User
	if err := ctrl.DB.Where("email = ?", loginDetails.Email).First(&user).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
		return
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(loginDetails.Password)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
		return
	}

	session, _ := ctrl.Store.Get(c.Request, "session-name")
	session.Values["user_id"] = user.ID
	session.Save(c.Request, c.Writer)

	c.Redirect(http.StatusFound, "/")
}

// LogoutUser handles user logout
func (ctrl *UserController) LogoutUser(c *gin.Context) {
	session, _ := ctrl.Store.Get(c.Request, "session-name")
	session.Values["user_id"] = nil
	session.Options.MaxAge = -1
	session.Save(c.Request, c.Writer)

	c.Redirect(http.StatusFound, "/")
}
