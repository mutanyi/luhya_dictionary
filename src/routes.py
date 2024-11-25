from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from models import User, DictionaryEntry, Dialect
from forms import LoginForm, RegistrationForm, WordEntryForm
from app import app, db
from sqlalchemy import or_

@app.route('/')
@app.route('/index')
def index():
    """Home page showing search interface and recent entries."""
    # Get available dialects for the filter
    dialects = Dialect.query.all()
    
    # Get recent published entries
    recent_entries = DictionaryEntry.query.filter_by(is_published=True)\
        .order_by(DictionaryEntry.created_at.desc())\
        .limit(10)\
        .all()
    
    return render_template('index.html', 
                         dialects=dialects,
                         recent_entries=recent_entries)

@app.route('/search')
def search():
    """Search dictionary entries."""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    if not query:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'entries': [],
                'total': 0,
                'pages': 0,
                'current_page': page
            })
        return render_template('search.html', entries=[], query='')
    
    try:
        # Search in both English and Luhya words
        entries = DictionaryEntry.query.filter(
            or_(
                DictionaryEntry.english_word.ilike(f'%{query}%'),
                DictionaryEntry.luhya_word.ilike(f'%{query}%')
            )
        ).order_by(DictionaryEntry.created_at.desc())
        
        # Get paginated results
        paginated_entries = entries.paginate(page=page, per_page=per_page, error_out=False)
        
        # Format entries for response
        formatted_entries = []
        for entry in paginated_entries.items:
            dialect = Dialect.query.get(entry.dialect_id)
            formatted_entries.append({
                'id': entry.id,
                'luhya_word': entry.luhya_word,
                'english_word': entry.english_word,
                'part_of_speech': entry.part_of_speech,
                'dialect': dialect.name if dialect else 'Unknown',
                'native_name': dialect.native_name if dialect else 'Unknown',
                'example_sentence': entry.example_sentence,
                'pronunciation_guide': entry.pronunciation_guide,
                'cultural_notes': entry.cultural_notes,
                'usage_notes': entry.usage_notes,
                'source': entry.source,
                'source_type': entry.source_type,
                'created_at': entry.created_at.strftime('%Y-%m-%d %H:%M:%S') if entry.created_at else None
            })
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'entries': formatted_entries,
                'total': paginated_entries.total,
                'pages': paginated_entries.pages,
                'current_page': page
            })
        
        return render_template('search.html', 
                             entries=formatted_entries,
                             query=query,
                             total=paginated_entries.total,
                             pages=paginated_entries.pages,
                             current_page=page)
                             
    except Exception as e:
        app.logger.error(f"Search error: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'An error occurred during search'}), 500
        flash('An error occurred during search. Please try again.', 'error')
        return render_template('search.html', entries=[], query=query)

@app.route('/dialects')
def dialects():
    """Get all dialects."""
    dialects = Dialect.query.all()
    return render_template('dialects.html', dialects=dialects)

@app.route('/dialect/<int:dialect_id>')
def view_dialect(dialect_id):
    """View details of a specific dialect."""
    dialect = Dialect.query.get_or_404(dialect_id)
    entries = DictionaryEntry.query.filter_by(dialect_id=dialect_id, is_published=True)\
        .order_by(DictionaryEntry.created_at.desc())\
        .all()
    return render_template('dialect.html', dialect=dialect, entries=entries)

@app.route('/entry/<int:entry_id>')
@app.route('/dictionary_entry/<int:entry_id>')
def view_entry(entry_id):
    """View details of a specific dictionary entry."""
    entry = DictionaryEntry.query.get_or_404(entry_id)
    return render_template('entry.html', entry=entry)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            institution=form.institution.data,
            credentials=form.credentials.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering! Please wait for admin approval.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    """Add a new dictionary entry."""
    if not current_user.is_verified:
        flash('Your account needs to be verified before you can add words.')
        return redirect(url_for('index'))
    
    form = WordEntryForm()
    
    if form.validate_on_submit():
        try:
            entry = DictionaryEntry(
                luhya_word=form.luhya_word.data,
                english_word=form.english_word.data,
                part_of_speech=form.part_of_speech.data,
                dialect_id=form.dialect.data,
                example_sentence=form.example_sentence.data,
                pronunciation_guide=form.pronunciation_guide.data,
                cultural_notes=form.cultural_notes.data,
                usage_notes=form.usage_notes.data,
                source=form.source.data,
                source_type=form.source_type.data,
                verification_notes=form.verification_notes.data,
                added_by_id=current_user.id,
                created_at=datetime.utcnow()
            )
            db.session.add(entry)
            db.session.commit()
            flash('Word added successfully! It will be reviewed by moderators.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding word: {str(e)}")
            flash('An error occurred while adding the word. Please try again.', 'error')
    
    return render_template('add_word.html', 
                         title='Add Word',
                         form=form)

@app.route('/admin')
@login_required
def admin():
    """Admin dashboard."""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('index'))
    pending_users = User.query.filter_by(is_verified=False).all()
    pending_entries = DictionaryEntry.query.filter_by(is_verified=False).all()
    return render_template('admin.html', 
                         title='Admin Dashboard',
                         pending_users=pending_users,
                         pending_entries=pending_entries)

@app.route('/verify_user/<int:user_id>', methods=['POST'])
@login_required
def verify_user(user_id):
    """Verify a user account."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    
    return jsonify({'message': 'User verified successfully'})

@app.route('/verify_entry/<int:entry_id>', methods=['POST'])
@login_required
def verify_entry(entry_id):
    """Verify a dictionary entry."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    entry = DictionaryEntry.query.get_or_404(entry_id)
    entry.is_verified = True
    entry.is_published = True
    entry.verified_by_id = current_user.id
    entry.verified_date = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Entry verified successfully'})
