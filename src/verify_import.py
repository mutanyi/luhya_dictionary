from app import app
from models import DictionaryEntry
import random

def verify_import():
    with app.app_context():
        # Get total count
        total = DictionaryEntry.query.count()
        print(f"Total entries in database: {total}")
        
        # Get 5 random entries
        entries = DictionaryEntry.query.order_by(DictionaryEntry.id).all()
        samples = random.sample(entries, 5)
        
        print("\nRandom sample of entries:")
        print("-" * 80)
        for entry in samples:
            print(f"Luhya Word: {entry.luhya_word}")
            print(f"English Word: {entry.english_word}")
            print(f"Part of Speech: {entry.part_of_speech}")
            print(f"Usage Notes: {entry.usage_notes}")
            print(f"Source: {entry.source}")
            print("-" * 80)

if __name__ == '__main__':
    verify_import()
