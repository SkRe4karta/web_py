from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    courses = CoursesFilter(**search_params()).perform()
    pagination = db.paginate(courses)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = db.get_or_404(Course, course_id)
    return render_template('courses/show.html', course=course)

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    from flask_login import current_user
    from sqlalchemy import desc, asc
    
    course = db.get_or_404(Course, course_id)
    
    # Получаем параметры сортировки
    sort = request.args.get('sort', 'newest')
    
    # Формируем запрос
    query = db.select(Review).where(Review.course_id == course_id)
    
    # Применяем сортировку
    if sort == 'newest':
        query = query.order_by(desc(Review.created_at))
    elif sort == 'positive':
        query = query.order_by(desc(Review.rating), desc(Review.created_at))
    elif sort == 'negative':
        query = query.order_by(asc(Review.rating), desc(Review.created_at))
    
    # Пагинация (по 5 отзывов на странице)
    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(query, page=page, per_page=5)
    reviews = pagination.items
    
    # Проверяем, оставлял ли текущий пользователь отзыв
    user_review = None
    if current_user.is_authenticated:
        user_review = db.session.execute(
            db.select(Review).where(
                Review.course_id == course_id,
                Review.user_id == current_user.id
            )
        ).scalar_one_or_none()
    
    return render_template('courses/reviews.html',
                         course=course,
                         reviews=reviews,
                         pagination=pagination,
                         sort=sort,
                         user_review=user_review)

@bp.route('/<int:course_id>/reviews/create', methods=['POST'])
@login_required
def create_review(course_id):
    from flask_login import current_user  # Добавьте эту строку
    
    course = db.get_or_404(Course, course_id)
    
    # Проверяем, не оставлял ли пользователь уже отзыв
    existing_review = db.session.execute(
        db.select(Review).where(
            Review.course_id == course_id,
            Review.user_id == current_user.id
        )
    ).scalar_one_or_none()
    
    if existing_review:
        flash('Вы уже оставили отзыв на этот курс', 'warning')
        return redirect(url_for('courses.show', course_id=course_id))
    
    # Получаем данные из формы
    rating = request.form.get('rating', type=int)
    text = request.form.get('text', '').strip()
    
    # Валидация
    if not text:
        flash('Текст отзыва не может быть пустым', 'danger')
        return redirect(url_for('courses.show', course_id=course_id))
    
    if rating is None or rating < 0 or rating > 5:
        flash('Некорректная оценка', 'danger')
        return redirect(url_for('courses.show', course_id=course_id))
    
    try:
        # Создаем отзыв
        review = Review(
            rating=rating,
            text=text,
            course_id=course_id,
            user_id=current_user.id
        )
        db.session.add(review)
        
        # Обновляем рейтинг курса
        course.rating_sum += rating
        course.rating_num += 1
        
        db.session.commit()
        flash('Ваш отзыв успешно добавлен!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при сохранении отзыва: {str(e)}', 'danger')
    
    return redirect(url_for('courses.show', course_id=course_id))