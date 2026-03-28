from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        (5, '5 — отлично'),
        (4, '4 — хорошо'),
        (3, '3 — удовлетворительно'),
        (2, '2 — неудовлетворительно'),
        (1, '1 — плохо'),
        (0, '0 — ужасно')
    ], coerce=int, validators=[DataRequired()])
    
    text = TextAreaField('Текст отзыва', validators=[
        DataRequired(),
        Length(min=5, max=1000)
    ])
    
    submit = SubmitField('Оставить отзыв')