package main

import (
	"log"
	"os"

	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/source/file"
)

func main() {
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		dbURL = "postgres://postgres:postgres@localhost:5432/ecommerce?sslmode=disable"
	}

	m, err := migrate.New(
		"file://migrations",
		dbURL,
	)
	if err != nil {
		log.Fatalf("❌ Failed to initialize migrate: %v", err)
	}
	defer func() {
		srcErr, dbErr := m.Close()
		if srcErr != nil || dbErr != nil {
			log.Printf("⚠️ Error closing migration resources: %v %v", srcErr, dbErr)
		}
	}()

	log.Println("🚀 Running migrations...")
	if err := m.Up(); err != nil {
		if err == migrate.ErrNoChange {
			log.Println("✅ Database already up to date.")
		} else {
			log.Fatalf("❌ Migration failed: %v", err)
		}
	} else {
		log.Println("✅ Migrations applied successfully!")
	}
}
