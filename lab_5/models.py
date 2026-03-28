from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Инициализация SQLAlchemy
db = SQLAlchemy()


class Role(db.Model):
    """Модель ролей пользователей (админ, пользователь, менеджер)"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # Связь с пользователями: одна роль может быть у многих пользователей
    users = db.relationship('User', backref='role', lazy=True)


class User(UserMixin, db.Model):
    """
    Модель пользователя
    Наследует UserMixin для интеграции с Flask-Login
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(80))
    first_name = db.Column(db.String(80), nullable=False)
    patronymic = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Хеширует пароль перед сохранением в базу"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверяет соответствие введённого пароля сохранённому хешу"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Возвращает полное ФИО пользователя или логин, если ФИО не указано"""
        parts = [self.last_name, self.first_name, self.patronymic]
        return ' '.join(p for p in parts if p) or self.login
    
    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        return self.role and self.role.name == 'admin'


class VisitLog(db.Model):
    """
    Модель журнала посещений
    Фиксирует каждый переход пользователя по страницам сайта
    """
    __tablename__ = 'visit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)  # Путь страницы
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ID пользователя (может быть NULL)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Дата и время посещения
    
    # Связь с пользователем для получения ФИО
    user = db.relationship('User', backref='visits')