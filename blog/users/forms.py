from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from blog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email is already used.')


    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your email is already used.')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Update Profile')