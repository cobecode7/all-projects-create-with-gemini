package controllers

import (
	"net/http"

	"gemini-project/models"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/sessions"
	"gorm.io/gorm"
)

// HomeController handles the home page
type HomeController struct {
	DB    *gorm.DB
	Store sessions.Store
}

// NewHomeController creates a new HomeController
func NewHomeController(db *gorm.DB, store sessions.Store) *HomeController {
	return &HomeController{DB: db, Store: store}
}

// ShowHome renders the home page
func (ctrl *HomeController) ShowHome(c *gin.Context) {
	session, _ := ctrl.Store.Get(c.Request, "session-name")
	userID := session.Values["user_id"]

	var user models.User
	if userID != nil {
		ctrl.DB.First(&user, userID)
	}

	c.HTML(http.StatusOK, "base.html", gin.H{
		"title": "Home",
		"user": user,
	})
}

// ShowDashboard renders the dashboard page (protected)
func (ctrl *HomeController) ShowDashboard(c *gin.Context) {
	session, _ := ctrl.Store.Get(c.Request, "session-name")
	userID := session.Values["user_id"]

	// Check if user is logged in
	if userID == nil {
		c.Redirect(http.StatusFound, "/login")
		return
	}

	var user models.User
	ctrl.DB.First(&user, userID)

	c.HTML(http.StatusOK, "dashboard.html", gin.H{
		"title": "Dashboard",
		"user": user,
	})
}
