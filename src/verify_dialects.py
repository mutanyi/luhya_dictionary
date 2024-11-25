from app import app
from models import Dialect

def verify_dialects():
    with app.app_context():
        dialects = Dialect.query.all()
        for dialect in dialects:
            print(f"{dialect.name} ({dialect.code})")
            print(f"  Ethnic Group: {dialect.ethnic_group}")
            print(f"  Regions: {dialect.regions}")
            print(f"  Description: {dialect.description}")
            print()

if __name__ == '__main__':
    verify_dialects()
