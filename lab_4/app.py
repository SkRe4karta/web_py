import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from flask_wtf import FlaskForm

# ----------------------------- Конфигурация -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ----------------------------- Модели -----------------------------
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(200))

    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.patronymic]
        return ' '.join(p for p in parts if p) or self.login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------------------- Формы и валидаторы -----------------------------
def password_complexity(form, field):
    password = field.data
    if not password:
        raise ValidationError('Пароль не может быть пустым')
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов')
    if len(password) > 128:
        raise ValidationError('Пароль должен содержать не более 128 символов')
    if not re.search(r'[A-ZА-Я]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву (латиницу или кириллицу)')
    if not re.search(r'[a-zа-я]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву (латиницу или кириллицу)')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')
    if re.search(r'\s', password):
        raise ValidationError('Пароль не должен содержать пробелов')
    allowed = r'^[A-Za-zА-Яа-я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|"\'.,:;]*$'
    if not re.match(allowed, password):
        raise ValidationError('Пароль содержит недопустимые символы')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class UserCreateForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(message='Логин не может быть пустым'),
        Length(min=5, message='Логин должен содержать не менее 5 символов'),
        Regexp('^[A-Za-z0-9]+$', message='Логин может содержать только латинские буквы и цифры')
    ])
    password = PasswordField('Пароль', validators=[password_complexity])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired(message='Имя не может быть пустым')])
    patronymic = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int, choices=[], validators=[])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = [(0, 'Без роли')]

class UserEditForm(FlaskForm):
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired(message='Имя не может быть пустым')])
    patronymic = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int, choices=[], validators=[])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = [(0, 'Без роли')]

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[password_complexity])
    confirm_password = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить пароль')

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Пароли не совпадают')

# ----------------------------- Вспомогательные функции -----------------------------
def populate_role_choices(form):
    roles = Role.query.all()
    form.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in roles]

# ----------------------------- Маршруты -----------------------------
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/user/<int:user_id>')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('view_user.html', user=user)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserCreateForm()
    populate_role_choices(form)
    if form.validate_on_submit():
        if User.query.filter_by(login=form.login.data).first():
            flash('Пользователь с таким логином уже существует.', 'danger')
            return render_template('create_user.html', form=form)
        user = User(
            login=form.login.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data or None,
            patronymic=form.patronymic.data or None,
            role_id=form.role_id.data if form.role_id.data != 0 else None
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь успешно создан.', 'success')
        return redirect(url_for('index'))
    return render_template('create_user.html', form=form)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm()
    populate_role_choices(form)
    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name or ''
        form.patronymic.data = user.patronymic or ''
        form.role_id.data = user.role_id if user.role_id is not None else 0
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data or None
        user.patronymic = form.patronymic.data or None
        user.role_id = form.role_id.data if form.role_id.data != 0 else None
        db.session.commit()
        flash('Данные пользователя обновлены.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_user.html', form=form, user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Запрет на удаление root
    if user.login == 'root':
        flash('Пользователь root защищён от удаления.', 'danger')
        return redirect(url_for('index'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удалён.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при удалении пользователя.', 'danger')
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Неверный старый пароль.', 'danger')
            return render_template('change_password.html', form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Пароль успешно изменён.', 'success')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Неверный логин или пароль.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ----------------------------- Инициализация базы данных -----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Создание ролей, если их нет
        if Role.query.count() == 0:
            roles = [
                Role(name='admin', description='Администратор'),
                Role(name='user', description='Обычный пользователь'),
                Role(name='manager', description='Менеджер')
            ]
            db.session.add_all(roles)
            db.session.commit()
            print("Роли добавлены.")
        
        # Создание пользователя root, если его нет
        if User.query.filter_by(login='root').first() is None:
            root = User(
                login='root',
                first_name='Root',
                last_name='User',
                role_id=admin_role.id if admin_role else None
            )
            root.set_password('Qwerty123')
            db.session.add(root)
            db.session.commit()я
            print("Пользователь root создан (логин: root, пароль: Qwerty123)")

    app.run(debug=True)