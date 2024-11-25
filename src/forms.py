from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, PasswordField, SelectField,
                    BooleanField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User, Dialect

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
    """Form for adding new dictionary entries."""
    luhya_word = StringField('Luhya Word', validators=[DataRequired()])
    english_word = StringField('English Translation', validators=[DataRequired()])
    part_of_speech = SelectField('Part of Speech', 
                               choices=[('noun', 'Noun'), ('verb', 'Verb'), 
                                      ('adjective', 'Adjective'), ('adverb', 'Adverb'),
                                      ('pronoun', 'Pronoun'), ('preposition', 'Preposition'),
                                      ('conjunction', 'Conjunction'), ('interjection', 'Interjection')],
                               validators=[DataRequired()])
    dialect = SelectField('Dialect', coerce=int, validators=[DataRequired()])
    example_sentence = TextAreaField('Example Sentence')
    pronunciation_guide = StringField('Pronunciation Guide')
    cultural_notes = TextAreaField('Cultural Notes')
    usage_notes = TextAreaField('Usage Notes')
    source = StringField('Source')
    source_type = SelectField('Source Type',
                            choices=[('oral', 'Oral'), ('written', 'Written'),
                                   ('academic', 'Academic'), ('other', 'Other')])
    verification_notes = TextAreaField('Verification Notes')
    submit = SubmitField('Submit Entry')

    def __init__(self, *args, **kwargs):
        super(WordEntryForm, self).__init__(*args, **kwargs)
        from models import Dialect
        # Get all dialects from database
        dialects = Dialect.query.order_by(Dialect.name).all()
        self.dialect.choices = [(d.id, f"{d.name} ({d.native_name})") for d in dialects]
        # Set default to Isukha
        isukha = Dialect.query.filter_by(name='Isukha').first()
        if isukha and not self.dialect.data:
            self.dialect.data = isukha.id
