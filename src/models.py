from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(120))
    institution = db.Column(db.String(120))
    credentials = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships with explicit foreign keys
    entries_added = db.relationship('DictionaryEntry',
                                  backref='added_by',
                                  foreign_keys='DictionaryEntry.added_by_id',
                                  lazy='dynamic')
    entries_verified = db.relationship('DictionaryEntry',
                                     backref='verified_by',
                                     foreign_keys='DictionaryEntry.verified_by_id',
                                     lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class DictionaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    luhya_word = db.Column(db.String(100), nullable=False)
    english_word = db.Column(db.String(100), nullable=False)
    part_of_speech = db.Column(db.String(50))
    example_sentence = db.Column(db.String(200))
    dialect = db.Column(db.String(50))
    source = db.Column(db.String(200))
    source_type = db.Column(db.String(50))
    pronunciation_guide = db.Column(db.String(100))
    cultural_notes = db.Column(db.Text)
    usage_notes = db.Column(db.Text)
    
    # Verification and tracking
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    verified_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    verified_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status tracking
    is_verified = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=False)
    verification_notes = db.Column(db.Text)

    def __repr__(self):
        return f'<DictionaryEntry {self.luhya_word}>'
