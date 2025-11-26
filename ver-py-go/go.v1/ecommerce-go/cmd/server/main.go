package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/yourusername/ecommerce-go/internal/config"
	"github.com/yourusername/ecommerce-go/internal/database"
	"github.com/yourusername/ecommerce-go/internal/handlers"
	"github.com/yourusername/ecommerce-go/internal/repository"
	"github.com/yourusername/ecommerce-go/internal/router"
)

func main() {
	cfg := config.LoadConfig()
	db := database.NewConnection(cfg.DBUrl)
	defer db.Close()

	userRepo := repository.NewUserRepository(db)
	authHandler := handlers.NewAuthHandler(userRepo)

	r := gin.Default()
	router.SetupRoutes(r, authHandler)

	srv := &http.Server{
		Addr:    ":" + cfg.ServerPort,
		Handler: r,
	}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("❌ Server error: %v", err)
		}
	}()

	log.Println("🚀 Server running on port", cfg.ServerPort)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt)
	<-quit

	log.Println("🧹 Gracefully shutting down...")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("✅ Server exited cleanly")
}
