from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(LoginForm):
    submit = SubmitField('Зарегистрироваться')

class EditTaskForm(FlaskForm):
    title = StringField('Название:', validators=[DataRequired()])
    points = StringField('Баллы:', validators=[DataRequired()])
    category = StringField('Категория:', validators=[DataRequired()])
    content = StringField('Формулировка:', validators=[DataRequired()])
    flag = StringField('Флаг:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class EnterFlagForm(FlaskForm):
    flag = StringField('', validators=[DataRequired()])
    submit = SubmitField('Проверить')