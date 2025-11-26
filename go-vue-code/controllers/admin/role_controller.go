package admin

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/go-vue-code/config"
	"github.com/go-vue-code/middleware"
	"github.com/go-vue-code/models"
)

// GetRoles retrieves all roles with pagination
func GetRoles(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "roles.view") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	// Get pagination parameters
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
	offset := (page - 1) * limit

	var roles []models.Role
	var total int64

	// Get roles with pagination
	config.DB.Model(&models.Role{}).Count(&total)
	config.DB.Preload("Permissions").Offset(offset).Limit(limit).Find(&roles)

	c.JSON(http.StatusOK, gin.H{
		"roles": roles,
		"total": total,
		"page":  page,
		"limit": limit,
	})
}

// GetRole retrieves a single role by ID
func GetRole(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "roles.view") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var role models.Role

	// Get role with permissions
	if err := config.DB.Preload("Permissions").First(&role, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Role not found"})
		return
	}

	c.JSON(http.StatusOK, role)
}

// CreateRole creates a new role
func CreateRole(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "roles.create") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	var input struct {
		Name          string `json:"name" binding:"required"`
		Description   string `json:"description"`
		PermissionIDs []uint `json:"permissionIds"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check if role name already exists
	var existingRole models.Role
	if err := config.DB.Where("name = ?", input.Name).First(&existingRole).Error; err == nil {
		c.JSON(http.StatusConflict, gin.H{"error": "Role name already exists"})
		return
	}

	// Create role
	role := models.Role{
		Name:        input.Name,
		Description: input.Description,
	}

	// Start transaction
	tx := config.DB.Begin()

	// Create role
	if err := tx.Create(&role).Error; err != nil {
		tx.Rollback()
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create role"})
		return
	}

	// Associate permissions
	if len(input.PermissionIDs) > 0 {
		var permissions []models.Permission
		if err := tx.Where("id IN ?", input.PermissionIDs).Find(&permissions).Error; err != nil {
			tx.Rollback()
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to find permissions"})
			return
		}

		if err := tx.Model(&role).Association("Permissions").Append(permissions); err != nil {
			tx.Rollback()
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to associate permissions"})
			return
		}
	}

	// Commit transaction
	if err := tx.Commit().Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create role"})
		return
	}

	// Get role with permissions
	config.DB.Preload("Permissions").First(&role, role.ID)

	c.JSON(http.StatusCreated, role)
}

// UpdateRole updates an existing role
func UpdateRole(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "roles.update") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var role models.Role

	if err := config.DB.First(&role, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Role not found"})
		return
	}

	var input struct {
		Name          string `json:"name"`
		Description   string `json:"description"`
		PermissionIDs []uint `json:"permissionIds"`
	}

	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Update fields if provided
	if input.Name != "" {
		// Check if role name already exists for another role
		var existingRole models.Role
		if err := config.DB.Where("name = ? AND id != ?", input.Name, role.ID).First(&existingRole).Error; err == nil {
			c.JSON(http.StatusConflict, gin.H{"error": "Role name already exists"})
			return
		}
		role.Name = input.Name
	}
	if input.Description != "" {
		role.Description = input.Description
	}

	// Start transaction
	tx := config.DB.Begin()

	// Update role
	if err := tx.Save(&role).Error; err != nil {
		tx.Rollback()
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update role"})
		return
	}

	// Update permissions if provided
	if input.PermissionIDs != nil {
		// Clear existing permissions
		if err := tx.Model(&role).Association("Permissions").Clear(); err != nil {
			tx.Rollback()
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to clear permissions"})
			return
		}

		// Add new permissions
		if len(input.PermissionIDs) > 0 {
			var permissions []models.Permission
			if err := tx.Where("id IN ?", input.PermissionIDs).Find(&permissions).Error; err != nil {
				tx.Rollback()
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to find permissions"})
				return
			}

			if err := tx.Model(&role).Association("Permissions").Append(permissions); err != nil {
				tx.Rollback()
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to associate permissions"})
				return
			}
		}
	}

	// Commit transaction
	if err := tx.Commit().Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update role"})
		return
	}

	// Get role with permissions
	config.DB.Preload("Permissions").First(&role, role.ID)

	c.JSON(http.StatusOK, role)
}

// DeleteRole deletes a role
func DeleteRole(c *gin.Context) {
	// Check if user has admin permission
	if !middleware.HasPermission(c, "roles.delete") {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}

	id := c.Param("id")
	var role models.Role

	if err := config.DB.First(&role, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Role not found"})
		return
	}

	// Check if role is assigned to any users
	var userCount int64
	config.DB.Model(&models.User{}).Where("role_id = ?", role.ID).Count(&userCount)
	if userCount > 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Cannot delete role assigned to users"})
		return
	}

	if err := config.DB.Delete(&role).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete role"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Role deleted successfully"})
}
