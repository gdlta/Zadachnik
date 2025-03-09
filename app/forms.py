from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Роль', choices=[('company', 'Компания'), ('employee', 'Сотрудник')], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Описание задачи', validators=[DataRequired(), Length(max=500)])
    category = StringField('Категория', validators=[DataRequired(), Length(max=50)])
    due_date = DateTimeField('Срок выполнения', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    is_completed = BooleanField('Задача выполнена')
    submit = SubmitField('Добавить задачу')