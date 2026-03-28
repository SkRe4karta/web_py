from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Role, VisitLog
from forms import LoginForm, UserCreateForm, UserEditForm, ChangePasswordForm
from decorators import admin_required
from utils import populate_role_choices
from stats import stats_bp

# ----------------------------- Инициализация приложения -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'

# Регистрация Blueprint для статистики
app.register_blueprint(stats_bp)


# ----------------------------- Загрузчик пользователя -----------------------------
@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя по ID из сессии (необходимо для Flask-Login)"""
    return User.query.get(int(user_id))


# ----------------------------- Автоматическая запись посещений -----------------------------
@app.before_request
def log_visit():
    """
    Автоматическая запись каждого посещения в журнал
    Срабатывает перед каждым запросом (кроме статических файлов)
    """
    if request.endpoint and not request.endpoint.startswith('static'):
        try:
            log = VisitLog(
                path=request.path,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            db.session.add(log)
            db.session.commit()
        except:
            db.session.rollback()  # Откат в случае ошибки


# ----------------------------- Маршруты CRUD для пользователей -----------------------------
@app.route('/')
def index():
    """Главная страница - список всех пользователей"""
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/user/<int:user_id>')
@login_required
def view_user(user_id):
    """
    Просмотр профиля пользователя
    - Администратор может смотреть любого
    - Обычный пользователь - только свой
    """
    user = User.query.get_or_404(user_id)
    if not current_user.is_admin and user.id != current_user.id:
        flash('У вас недостаточно прав для просмотра этого профиля.', 'danger')
        return redirect(url_for('index'))
    return render_template('view_user.html', user=user)


@app.route('/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """
    Создание нового пользователя
    Доступно только администраторам
    """
    form = UserCreateForm()
    populate_role_choices(form)
    
    if form.validate_on_submit():
        # Проверка уникальности логина
        if User.query.filter_by(login=form.login.data).first():
            flash('Пользователь с таким логином уже существует.', 'danger')
        else:
            # Создание пользователя
            user = User(
                login=form.login.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data or None,
                patronymic=form.patronymic.data or None,
                role_id=form.role_id.data if form.role_id.data else None
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
    """
    Редактирование пользователя
    - Администратор может редактировать любого
    - Обычный пользователь - только себя (без смены роли)
    """
    user = User.query.get_or_404(user_id)
    
    # Проверка прав на редактирование
    if not current_user.is_admin and user.id != current_user.id:
        flash('У вас недостаточно прав для редактирования этого профиля.', 'danger')
        return redirect(url_for('index'))
    
    form = UserEditForm()
    populate_role_choices(form)
    
    # Заполнение формы текущими данными
    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name or ''
        form.patronymic.data = user.patronymic or ''
        form.role_id.data = user.role_id or 0
    
    # Обработка отправленной формы
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data or None
        user.patronymic = form.patronymic.data or None
        
        # Только администратор может менять роль
        if current_user.is_admin:
            user.role_id = form.role_id.data if form.role_id.data else None
        
        db.session.commit()
        flash('Данные пользователя обновлены.', 'success')
        return redirect(url_for('index'))
    
    return render_template(
        'edit_user.html', 
        form=form, 
        user=user, 
        is_admin=current_user.is_admin
    )


@app.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """
    Удаление пользователя
    Доступно только администраторам
    Root пользователь защищён от удаления
    """
    user = User.query.get_or_404(user_id)
    
    if user.login == 'root':
        flash('Пользователь root защищён от удаления.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удалён.', 'success')
    
    return redirect(url_for('index'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Смена пароля текущего пользователя"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Неверный старый пароль.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль успешно изменён.', 'success')
            return redirect(url_for('index'))
    
    return render_template('change_password.html', form=form)


# ----------------------------- Аутентификация -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Неверный логин или пароль.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('index'))


# ----------------------------- Инициализация базы данных -----------------------------
def init_database():
    """
    Создание таблиц и начальных данных
    Выполняется при первом запуске приложения
    """
    with app.app_context():
        db.create_all()
        
        # Создание ролей, если их нет
        if not Role.query.first():
            roles = [
                Role(name='admin', description='Администратор'),
                Role(name='user', description='Пользователь'),
                Role(name='manager', description='Менеджер')
            ]
            db.session.add_all(roles)
            db.session.commit()
            print('Роли созданы')
        
        # Создание root пользователя, если его нет
        if not User.query.filter_by(login='root').first():
            admin_role = Role.query.filter_by(name='admin').first()
            root = User(
                login='root',
                first_name='Root',
                last_name='User',
                role_id=admin_role.id if admin_role else None
            )
            root.set_password('Qwerty123')
            db.session.add(root)
            db.session.commit()
            print('Пользователь root создан (логин: root, пароль: Qwerty123)')


# Запуск инициализации базы данных
init_database()

if __name__ == '__main__':
    app.run(debug=True)