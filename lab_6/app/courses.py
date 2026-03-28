from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver
from forms import ReviewForm

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = ['author_id', 'name', 'category_id', 'short_desc', 'full_desc']

def params():
    return {p: request.form.get(p) or None for p in COURSE_PARAMS}

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
        flash(f'Возникла ошибка при записи данных в БД. ({err})', 'danger')
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
    recent_reviews = Review.query.filter_by(course_id=course.id).order_by(desc(Review.created_at)).limit(5).all()
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(course_id=course.id, user_id=current_user.id).first()
    form = ReviewForm()
    return render_template('courses/show.html', course=course, recent_reviews=recent_reviews,
                         user_review=user_review, form=form)

@bp.route('/<int:course_id>/reviews')
def reviews_list(course_id):
    course = db.get_or_404(Course, course_id)
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'newest')
    query = Review.query.filter_by(course_id=course.id)
    if sort == 'positive':
        query = query.order_by(desc(Review.rating), desc(Review.created_at))
    elif sort == 'negative':
        query = query.order_by(asc(Review.rating), desc(Review.created_at))
    else:
        query = query.order_by(desc(Review.created_at))
    pagination = query.paginate(page=page, per_page=5, error_out=False)
    reviews = pagination.items
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(course_id=course.id, user_id=current_user.id).first()
    form = ReviewForm()
    return render_template('courses/reviews.html', course=course, reviews=reviews,
                         pagination=pagination, current_sort=sort, user_review=user_review, form=form)

@bp.route('/<int:course_id>/reviews', methods=['POST'])
@login_required
def add_review(course_id):
    course = db.get_or_404(Course, course_id)
    form = ReviewForm()
    if form.validate_on_submit():
        existing_review = Review.query.filter_by(course_id=course.id, user_id=current_user.id).first()
        if existing_review:
            flash('Вы уже оставили отзыв на этот курс', 'warning')
            return redirect(url_for('courses.reviews_list', course_id=course.id))
        review = Review(rating=form.rating.data, text=form.text.data, course_id=course.id, user_id=current_user.id)
        course.rating_sum += review.rating
        course.rating_num += 1
        if course.rating_num > 0:
            course.rating = course.rating_sum / course.rating_num
        db.session.add(review)
        db.session.commit()
        flash('Отзыв успешно добавлен!', 'success')
        return redirect(url_for('courses.reviews_list', course_id=course.id))
    return redirect(url_for('courses.reviews_list', course_id=course.id))

@bp.route('/<int:course_id>/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(course_id, review_id):
    review = db.get_or_404(Review, review_id)
    if review.user_id != current_user.id:
        flash('Вы можете удалять только свои отзывы', 'danger')
        return redirect(url_for('courses.reviews_list', course_id=course_id))
    course = review.course
    course.rating_sum -= review.rating
    course.rating_num -= 1
    if course.rating_num > 0:
        course.rating = course.rating_sum / course.rating_num
    else:
        course.rating = 0
    db.session.delete(review)
    db.session.commit()
    flash('Отзыв успешно удален', 'success')
    return redirect(url_for('courses.reviews_list', course_id=course_id))