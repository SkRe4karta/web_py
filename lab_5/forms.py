"""
Модуль forms.py - Определение форм для ввода данных
Содержит валидаторы и все формы приложения
"""

import re
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from flask_wtf import FlaskForm


def password_complexity(form, field):
    """
    Валидатор сложности пароля
    Проверяет: длина 8-128 символов, наличие заглавных/строчных букв, цифр, отсутствие пробелов
    """
    pwd = field.data
    if not pwd:
        raise ValidationError('Пароль не может быть пустым')
    if len(pwd) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов')
    if len(pwd) > 128:
        raise ValidationError('Пароль должен содержать не более 128 символов')
    if not re.search(r'[A-ZА-Я]', pwd):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    if not re.search(r'[a-zа-я]', pwd):
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву')
    if not re.search(r'[0-9]', pwd):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')
    if re.search(r'\s', pwd):
        raise ValidationError('Пароль не должен содержать пробелов')


class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UserCreateForm(FlaskForm):
    """Форма создания нового пользователя (только для администратора)"""
    login = StringField('Логин', validators=[
        DataRequired(message='Логин не может быть пустым'),
        Length(min=5, message='Логин должен содержать не менее 5 символов'),
        Regexp('^[A-Za-z0-9]+$', message='Логин может содержать только латинские буквы и цифры')
    ])
    password = PasswordField('Пароль', validators=[password_complexity])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired(message='Имя не может быть пустым')])
    patronymic = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int, choices=[])
    submit = SubmitField('Сохранить')


class UserEditForm(FlaskForm):
    """Форма редактирования пользователя (без смены пароля)"""
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired(message='Имя не может быть пустым')])
    patronymic = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int, choices=[])
    submit = SubmitField('Сохранить')


class ChangePasswordForm(FlaskForm):
    """Форма смены пароля с проверкой старого пароля"""
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[password_complexity])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить пароль')
    
    def validate_confirm_password(self, field):
        """Проверка совпадения нового пароля и его подтверждения"""
        if field.data != self.new_password.data:
            raise ValidationError('Пароли не совпадают')