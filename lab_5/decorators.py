from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(func):
    """
    Декоратор для проверки прав администратора
    Если пользователь не авторизован или не является администратором:
    - Выводится сообщение об ошибке
    - Выполняется перенаправление на главную страницу
    """
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper