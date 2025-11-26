package admin

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/go-vue-code/config"
	"github.com/go-vue-code/middleware"
	"github.com/go-vue-code/models"
)

// GetPermissions retrieves all permissions with pagination
func GetPermissions(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.view") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	// Get pagination parameters
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
	offset := (page - 1) * limit

	var permissions []models.Permission
	var total int64

	// Get permissions with pagination
	config.DB.Model(&models.Permission{}).Count(&total)
	config.DB.Offset(offset).Limit(limit).Find(&permissions)

	c.JSON(http.StatusOK, gin.H{
		"permissions": permissions,
		"total":       total,
		"page":        page,
		"limit":       limit,
	})
}

// GetPermission retrieves a single permission by ID
func GetPermission(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.view") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var permission models.Permission

	if err := config.DB.First(&permission, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Permission not found"})
		return
	}

	c.JSON(http.StatusOK, permission)
}

// CreatePermission creates a new permission
func CreatePermission(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.create") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	var input struct {
		Name        string `json:"name" binding:"required"`
		Description string `json:"description"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check if permission name already exists
	var existingPermission models.Permission
	if err := config.DB.Where("name = ?", input.Name).First(&existingPermission).Error; err == nil {
		c.JSON(http.StatusConflict, gin.H{"error": "Permission name already exists"})
		return
	}

	// Create permission
	permission := models.Permission{
		Name:        input.Name,
		Description: input.Description,
	}

	if err := config.DB.Create(&permission).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create permission"})
		return
	}

	c.JSON(http.StatusCreated, permission)
}

// UpdatePermission updates an existing permission
func UpdatePermission(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.update") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var permission models.Permission

	if err := config.DB.First(&permission, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Permission not found"})
		return
	}

	var input struct {
		Name        string `json:"name"`
		Description string `json:"description"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Update fields if provided
	if input.Name != "" {
		// Check if permission name already exists for another permission
		var existingPermission models.Permission
		if err := config.DB.Where("name = ? AND id != ?", input.Name, permission.ID).First(&existingPermission).Error; err == nil {
			c.JSON(http.StatusConflict, gin.H{"error": "Permission name already exists"})
			return
		}
		permission.Name = input.Name
	}
	if input.Description != "" {
		permission.Description = input.Description
	}

	if err := config.DB.Save(&permission).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update permission"})
		return
	}

	c.JSON(http.StatusOK, permission)
}

// DeletePermission deletes a permission
func DeletePermission(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.delete") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var permission models.Permission

	if err := config.DB.First(&permission, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Permission not found"})
		return
	}

	// Check if permission is assigned to any roles
	var roleCount int64
	config.DB.Table("role_permissions").Where("permission_id = ?", permission.ID).Count(&roleCount)
	if roleCount > 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Cannot delete permission assigned to roles"})
		return
	}

	if err := config.DB.Delete(&permission).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete permission"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Permission deleted successfully"})
}

// GetPermissionGroups retrieves permissions grouped by resource
func GetPermissionGroups(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "permissions.view") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	var permissions []models.Permission
	config.DB.Find(&permissions)

	// Group permissions by resource
	groups := make(map[string][]models.Permission)
	for _, permission := range permissions {
		// Extract resource from permission name (e.g., "users.view" -> "users")
		resource := permission.Name
		if len(resource) > 0 && resource[len(resource)-1] != '.' {
			for i := len(resource) - 1; i >= 0; i-- {
				if resource[i] == '.' {
					resource = resource[:i]
					break
				}
			}
		}

		groups[resource] = append(groups[resource], permission)
	}

	c.JSON(http.StatusOK, groups)
}
