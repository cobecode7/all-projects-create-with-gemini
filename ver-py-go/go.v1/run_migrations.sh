#!/usr/bin/env bash
set -e

# ────────────────────────────────
# إعداد المتغيرات
# ────────────────────────────────
DB_URL=${DATABASE_URL:-"postgres://postgres:postgres@localhost:5432/ecommerce?sslmode=disable"}
MIGRATIONS_DIR="./migrations"

echo "🚀 Running migrations on database: $DB_URL"

# تحقق من وجود psql
if ! command -v psql >/dev/null 2>&1; then
  echo "❌ Error: psql not found. Please install PostgreSQL client tools."
  exit 1
fi

# تحقق من وجود مجلد المهاجرات
if [ ! -d "$MIGRATIONS_DIR" ]; then
  echo "❌ Error: migrations directory not found!"
  exit 1
fi

# ────────────────────────────────
# تشغيل كل ملفات SQL
# ────────────────────────────────
for file in "$MIGRATIONS_DIR"/*.sql; do
  echo "📦 Applying migration: $(basename "$file")"
  psql "$DB_URL" -f "$file"
done

echo "✅ All migrations applied successfully!"
