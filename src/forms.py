from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, PasswordField, SelectField,
                    BooleanField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
                            validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    institution = StringField('Institution/Organization')
    credentials = TextAreaField('Academic/Professional Credentials')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class WordEntryForm(FlaskForm):
    luhya_word = StringField('Luhya Word', validators=[DataRequired()])
    english_word = StringField('English Translation', validators=[DataRequired()])
    part_of_speech = SelectField('Part of Speech', 
                               choices=[
                                   ('noun', 'Noun'),
                                   ('verb', 'Verb'),
                                   ('adjective', 'Adjective'),
                                   ('adverb', 'Adverb'),
                                   ('pronoun', 'Pronoun'),
                                   ('preposition', 'Preposition'),
                                   ('conjunction', 'Conjunction'),
                                   ('interjection', 'Interjection'),
                                   ('number', 'Number'),
                                   ('greeting', 'Greeting')
                               ])
    dialect = SelectField('Dialect',
                         choices=[
                             ('maragoli', 'Maragoli'),
                             ('bukusu', 'Bukusu'),
                             ('tachoni', 'Tachoni'),
                             ('idakho', 'Idakho'),
                             ('isukha', 'Isukha'),
                             ('other', 'Other')
                         ])
    example_sentence = TextAreaField('Example Sentence', validators=[DataRequired()])
    pronunciation_guide = StringField('Pronunciation Guide')
    cultural_notes = TextAreaField('Cultural Notes')
    usage_notes = TextAreaField('Usage Notes')
    source = StringField('Source', validators=[DataRequired()])
    source_type = SelectField('Source Type',
                            choices=[
                                ('academic', 'Academic Publication'),
                                ('community', 'Community Expert'),
                                ('literature', 'Literature'),
                                ('oral', 'Oral History'),
                                ('other', 'Other')
                            ])
    verification_notes = TextAreaField('Verification Notes')
    submit = SubmitField('Submit Entry')
