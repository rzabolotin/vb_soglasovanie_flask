from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators = [DataRequired()], render_kw = {'class':'form-control'})
    password = PasswordField('Пароль', validators = [DataRequired()], render_kw = {'class':'form-control'})
    remember_me = BooleanField("Запомнить меня", default=True, render_kw={'class':'form-check-input'})
    submit = SubmitField('Отправить', render_kw = {'class':'btn btn-primary'})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators = [DataRequired()], render_kw = {'class':'form-control'})
    email = StringField('Электронная почта', validators = [DataRequired(), Email()], render_kw = {'class':'form-control'})
    password = PasswordField('Пароль', validators = [DataRequired()], render_kw = {'class':'form-control'})
    password2 = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')], render_kw = {'class':'form-control'})
    submit = SubmitField('Отправить', render_kw = {'class':'btn btn-primary'})

    def validate_username(self, username):
        finded_users = User.query.filter_by(username = username.data).count()
        if finded_users: 
            raise ValidationError('Уже есть пользователь с именем {}'.format(username.data))

    def validate_email(self, email):
        finded_users = User.query.filter_by(email = email.data).count()
        if finded_users: 
            raise ValidationError('Уже есть пользователь с почтой {}'.format(email.data))


