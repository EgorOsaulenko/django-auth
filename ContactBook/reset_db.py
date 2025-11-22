"""
Скрипт для скидання бази даних та створення заново.
УВАГА: Це видалить всі дані з бази даних!
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "db.sqlite3"

if db_path.exists():
    print(f"Знайдено базу даних: {db_path}")
    response = input("Видалити базу даних? (yes/no): ")
    if response.lower() == 'yes':
        db_path.unlink()
        print("✓ База даних видалена")
        print("\nТепер виконайте:")
        print("  python manage.py migrate")
        print("  python manage.py createsuperuser")
    else:
        print("Операцію скасовано")
else:
    print("База даних не знайдена")
    print("\nВиконайте:")
    print("  python manage.py migrate")
    print("  python manage.py createsuperuser")


