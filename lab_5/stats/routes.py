import csv
from io import BytesIO, StringIO
from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from sqlalchemy import func
from models import db, VisitLog, User
from stats import stats_bp


@stats_bp.route('/logs')
@login_required
def logs():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    if current_user.is_admin:
        query = VisitLog.query
    else:
        query = VisitLog.query.filter_by(user_id=current_user.id)
    
    pagination = query.order_by(VisitLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('logs.html', logs=pagination.items, pagination=pagination)


@stats_bp.route('/pages-report')
@login_required
def pages_report():
    if not current_user.is_admin:
        flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
        return redirect(url_for('index'))
    
    results = db.session.query(
        VisitLog.path, 
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()
    
    return render_template('pages_report.html', results=results)


@stats_bp.route('/pages-report/export')
@login_required
def export_pages_report():
    if not current_user.is_admin:
        flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
        return redirect(url_for('index'))
    
    results = db.session.query(
        VisitLog.path, 
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()
    
    # Используем StringIO для текстовых данных
    si = StringIO()
    writer = csv.writer(si, delimiter=';')
    writer.writerow(['Страница', 'Количество посещений'])
    writer.writerows([[row.path, row.count] for row in results])
    
    # Конвертируем в bytes для отправки
    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name='pages_report.csv', 
        mimetype='text/csv'
    )


@stats_bp.route('/users-report')
@login_required
def users_report():
    if not current_user.is_admin:
        flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
        return redirect(url_for('index'))
    
    results = db.session.query(
        User, 
        func.count(VisitLog.id).label('count')
    ).outerjoin(VisitLog, User.id == VisitLog.user_id).group_by(User.id).order_by(
        func.count(VisitLog.id).desc()
    ).all()
    
    return render_template('users_report.html', results=results)


@stats_bp.route('/users-report/export')
@login_required
def export_users_report():
    if not current_user.is_admin:
        flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
        return redirect(url_for('index'))
    
    results = db.session.query(
        User, 
        func.count(VisitLog.id).label('count')
    ).outerjoin(VisitLog, User.id == VisitLog.user_id).group_by(User.id).order_by(
        func.count(VisitLog.id).desc()
    ).all()
    
    # Используем StringIO для текстовых данных
    si = StringIO()
    writer = csv.writer(si, delimiter=';')
    writer.writerow(['Пользователь', 'Количество посещений'])
    for user, count in results:
        user_name = user.full_name if user else 'Неаутентифицированный пользователь'
        writer.writerow([user_name, count])
    
    # Конвертируем в bytes для отправки
    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name='users_report.csv', 
        mimetype='text/csv'
    )