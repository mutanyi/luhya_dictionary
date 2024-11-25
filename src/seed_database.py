import os
import re
from datetime import datetime
from app import app, db
from models import User, DictionaryEntry

def parse_dictionary_entry(entry_text):
    """Parse a dictionary entry from the text file."""
    # Regular expression to match word, part of speech, and definition
    match = re.match(r'(\w+)\s+([n|v|adj|adv|prep|pron|vp|np|\.]+\.)\s+(.*)', entry_text)
    if match:
        word, pos, definition = match.groups()
        return {
            'luhya_word': word.strip(),
            'part_of_speech': pos.strip(),
            'english_word': definition.split(';')[0].strip(),  # Take first translation
            'usage_notes': definition.strip()
        }
    return None

def seed_database():
    """Seed the database with Luhya words from the text file."""
    with app.app_context():
        # Create all database tables
        db.drop_all()  # Drop existing tables
        db.create_all()  # Create fresh tables
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='Administrator',
                is_admin=True,
                is_verified=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

        # Read and parse the dictionary file
        file_path = os.path.join(app.root_path, '..', 'documents', 'Luhya_words.txt')
        current_entry = []
        entries_added = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines and page numbers
                if not line or line.isdigit() or line.startswith('Luwanga-English Dictionary'):
                    continue

                # If line starts with a Luhya word pattern (word followed by n., v., adj., etc.)
                if re.match(r'^\w+\s+[n|v|adj|adv|prep|pron|vp|np|\.]+\.', line):
                    # Process previous entry if exists
                    if current_entry:
                        entry_text = ' '.join(current_entry)
                        parsed_entry = parse_dictionary_entry(entry_text)
                        if parsed_entry:
                            # Create new dictionary entry
                            entry = DictionaryEntry(
                                luhya_word=parsed_entry['luhya_word'],
                                english_word=parsed_entry['english_word'],
                                part_of_speech=parsed_entry['part_of_speech'],
                                usage_notes=parsed_entry['usage_notes'],
                                dialect='Luwanga',  # Default dialect from the source
                                added_by_id=admin.id,
                                verified_by_id=admin.id,  # Auto-verify entries from the source
                                is_verified=True,
                                is_published=True,
                                verified_date=datetime.utcnow(),
                                source='Luwanga-English Dictionary (Appleby 1943, Anangwe 2006)',
                                source_type='academic'
                            )
                            db.session.add(entry)
                            entries_added += 1
                            
                            # Commit every 100 entries to avoid memory issues
                            if entries_added % 100 == 0:
                                db.session.commit()
                                print(f"Added {entries_added} entries...")
                    
                    current_entry = [line]
                else:
                    # Continue previous entry
                    current_entry.append(line)

        # Process the last entry
        if current_entry:
            entry_text = ' '.join(current_entry)
            parsed_entry = parse_dictionary_entry(entry_text)
            if parsed_entry:
                entry = DictionaryEntry(
                    luhya_word=parsed_entry['luhya_word'],
                    english_word=parsed_entry['english_word'],
                    part_of_speech=parsed_entry['part_of_speech'],
                    usage_notes=parsed_entry['usage_notes'],
                    dialect='Luwanga',
                    added_by_id=admin.id,
                    verified_by_id=admin.id,
                    is_verified=True,
                    is_published=True,
                    verified_date=datetime.utcnow(),
                    source='Luwanga-English Dictionary (Appleby 1943, Anangwe 2006)',
                    source_type='academic'
                )
                db.session.add(entry)
                entries_added += 1

        # Final commit
        db.session.commit()
        print(f"Successfully added {entries_added} Luhya words to the database!")

if __name__ == '__main__':
    seed_database()
