"""
Модуль utils.py - Вспомогательные функции
Содержит функции для заполнения выпадающих списков и другие утилиты
"""

from models import Role


def populate_role_choices(form):
    """
    Заполняет выпадающий список ролей в формах
    Формирует список: [(0, 'Без роли'), (1, 'admin'), (2, 'user'), ...]
    """
    roles = Role.query.all()
    form.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in roles]