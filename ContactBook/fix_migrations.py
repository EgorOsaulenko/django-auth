"""
Скрипт для виправлення проблеми з міграціями.
Це створить директорію static та дасть інструкції для виправлення міграцій.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Створюємо директорію static
static_dir = BASE_DIR / "static"
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Створено директорію: {static_dir}")

print("\n" + "="*60)
print("ІНСТРУКЦІЇ ДЛЯ ВИПРАВЛЕННЯ МІГРАЦІЙ:")
print("="*60)
print("\nПроблема: InconsistentMigrationHistory")
print("Міграція admin.0001_initial застосована раніше, ніж UserManager.0001_initial")
print("\nВаріанти вирішення:")
print("\n1. ВАРІАНТ 1 (рекомендовано для розробки):")
print("   Видалити базу даних і створити заново:")
print("   - Видалити файл: db.sqlite3")
print("   - Виконати: python manage.py migrate")
print("\n2. ВАРІАНТ 2 (якщо потрібно зберегти дані):")
print("   Виправити таблицю django_migrations вручну:")
print("   - Відкрити db.sqlite3 в SQLite браузері")
print("   - Видалити запис про admin.0001_initial")
print("   - Виконати: python manage.py migrate --fake-initial")
print("\n" + "="*60)


