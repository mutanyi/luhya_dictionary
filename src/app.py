from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///luhya_dictionary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
from database import db
db.init_app(app)
migrate = Migrate(app, db)

# Initialize login manager
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = 'info'

@login.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

def init_db():
    """Initialize the database with required tables and default data."""
    with app.app_context():
        db.create_all()
        
        # Import models here to avoid circular imports
        from models import User, Dialect
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='System Administrator',
                is_admin=True,
                is_verified=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            
            # Add default dialects with proper names
            default_dialects = [
                ('Isukha', 'Olushisha'),
                ('Bukusu', 'Lubukusu'),
                ('Idakho', 'Lwidakho'),
                ('Kabras', 'Lukabarasi'),
                ('Khayo', 'Olukhayo'),
                ('Kisa', 'Olushisa'),
                ('Marachi', 'Olumarachi'),
                ('Maragoli', 'Lulogoli'),
                ('Nyala', 'Olunyala'),
                ('Nyore', 'Olunyole'),
                ('Samia', 'Olusamia'),
                ('Tachoni', 'Olutachoni'),
                ('Tiriki', 'Lutiriki'),
                ('Tsotso', 'Olutsotso'),
                ('Wanga', 'Oluwanga')
            ]
            
            for name, native_name in default_dialects:
                if not Dialect.query.filter_by(name=name).first():
                    dialect = Dialect(name=name, native_name=native_name)
                    db.session.add(dialect)
            
            db.session.commit()

# Import routes after app is created to avoid circular imports
from routes import *

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)