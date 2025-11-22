"""Скрипт для створення директорії static"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"

if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)
    print(f"Створено директорію: {static_dir}")
else:
    print(f"Директорія вже існує: {static_dir}")


