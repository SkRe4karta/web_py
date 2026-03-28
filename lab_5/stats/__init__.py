"""
Модуль stats/__init__.py - Инициализация Blueprint для статистики
Создаёт Blueprint с префиксом /stats для всех маршрутов статистики
"""

from flask import Blueprint

# Создание Blueprint с префиксом URL /stats
stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

# Импорт маршрутов (после создания Blueprint, чтобы избежать циклических импортов)
from stats import routes