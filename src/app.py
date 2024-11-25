from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime
import os

from database import db
from models import User, DictionaryEntry
from forms import LoginForm, RegistrationForm, WordEntryForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                   full_name=form.full_name.data, institution=form.institution.data,
                   credentials=form.credentials.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering! Please wait for admin approval.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))
    pending_users = User.query.filter_by(is_verified=False).all()
    pending_entries = DictionaryEntry.query.filter_by(is_verified=False).all()
    return render_template('admin.html', pending_users=pending_users,
                         pending_entries=pending_entries)

@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    if not current_user.is_verified:
        flash('Your account needs to be verified before you can add words.')
        return redirect(url_for('home'))
    
    form = WordEntryForm()
    if form.validate_on_submit():
        entry = DictionaryEntry(
            luhya_word=form.luhya_word.data,
            english_word=form.english_word.data,
            part_of_speech=form.part_of_speech.data,
            dialect=form.dialect.data,
            example_sentence=form.example_sentence.data,
            pronunciation_guide=form.pronunciation_guide.data,
            cultural_notes=form.cultural_notes.data,
            usage_notes=form.usage_notes.data,
            source=form.source.data,
            source_type=form.source_type.data,
            verification_notes=form.verification_notes.data,
            added_by_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Word added successfully! It will be reviewed by moderators.')
        return redirect(url_for('home'))
    return render_template('add_word.html', title='Add Word', form=form)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    dialect = request.args.get('dialect', '')
    
    base_query = DictionaryEntry.query.filter(
        (DictionaryEntry.luhya_word.ilike(f'%{query}%')) |
        (DictionaryEntry.english_word.ilike(f'%{query}%'))
    ).filter_by(is_published=True)
    
    if dialect:
        base_query = base_query.filter(DictionaryEntry.dialect == dialect)
    
    entries = base_query.all()
    
    results = [{
        'luhya_word': entry.luhya_word,
        'english_word': entry.english_word,
        'part_of_speech': entry.part_of_speech,
        'example_sentence': entry.example_sentence,
        'dialect': entry.dialect,
        'source': entry.source,
        'pronunciation_guide': entry.pronunciation_guide,
        'cultural_notes': entry.cultural_notes,
        'usage_notes': entry.usage_notes
    } for entry in entries]
    
    return jsonify(results)

@app.route('/verify_entry/<int:id>', methods=['POST'])
@login_required
def verify_entry(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    entry = DictionaryEntry.query.get_or_404(id)
    entry.is_verified = True
    entry.is_published = True
    entry.verified_by_id = current_user.id
    entry.verified_date = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Entry verified successfully'})

@app.route('/verify_user/<int:id>', methods=['POST'])
@login_required
def verify_user(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(id)
    user.is_verified = True
    db.session.commit()
    
    return jsonify({'message': 'User verified successfully'})

def init_db():
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin',
                        email='admin@example.com',
                        full_name='Administrator',
                        is_admin=True,
                        is_verified=True)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
