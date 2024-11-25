from app import app, db
from models import DictionaryEntry, Dialect
import re
from datetime import datetime

def clean_text(text):
    """Clean up text by removing multiple spaces and newlines."""
    return ' '.join(text.strip().split())

def parse_entry(line):
    """Parse a dictionary entry line into components."""
    # Skip empty lines or section headers
    if not line.strip() or line.strip().isdigit() or 'Dictionary' in line:
        return None
    
    # Try to match the pattern: word part_of_speech definition
    match = re.match(r'(\S+)\s+((?:n\.|v\.(?:tr|int|refl)|adj\.|adv\.|prep\.|poss\.|np|vp|pron\.|conj\.|interj\.)\.?)\s+(.+)', line)
    if match:
        word = match.group(1)
        part_of_speech = match.group(2).rstrip('.')  # Remove trailing period
        definition = clean_text(match.group(3))
        return word, part_of_speech, definition
    
    # If no part of speech, treat the first word as the term and the rest as definition
    parts = line.split(None, 1)
    if len(parts) == 2:
        return parts[0], '', clean_text(parts[1])
    
    return None

def import_words():
    with app.app_context():
        # Get the Oluwanga dialect (since this is a Luwanga dictionary)
        dialect = Dialect.query.filter_by(code='oluwanga').first()
        if not dialect:
            print("Error: Oluwanga dialect not found in database")
            return

        # Read and process the dictionary file
        with open('/home/mutanyi/AI_Assistant_2024/luhya_dictionary/documents/Luhya_words.txt', 'r') as f:
            lines = f.readlines()

        # Skip the header (first few lines)
        start_index = 0
        for i, line in enumerate(lines):
            if 'amafumala' in line:  # First actual entry
                start_index = i
                break

        entries_added = 0
        for line in lines[start_index:]:
            parsed = parse_entry(line.strip())
            if parsed:
                luhya_word, part_of_speech, definition = parsed
                
                # Check if entry already exists
                existing = DictionaryEntry.query.filter_by(
                    luhya_word=luhya_word,
                    dialect_id=dialect.id
                ).first()
                
                if not existing:
                    entry = DictionaryEntry(
                        luhya_word=luhya_word,
                        english_word=definition.split(';')[0].strip(),  # Take first definition as English word
                        part_of_speech=part_of_speech,
                        usage_notes=definition,  # Store full definition in usage notes
                        dialect_id=dialect.id,
                        added_by_id=1,  # Admin user
                        verified_by_id=1,  # Admin user
                        verified_date=datetime.utcnow(),
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                        is_verified=True,
                        is_published=True,
                        source='Luwanga-English Dictionary (2008)',
                        source_type='Academic'
                    )
                    db.session.add(entry)
                    entries_added += 1
                    
                    # Commit every 100 entries to avoid memory issues
                    if entries_added % 100 == 0:
                        db.session.commit()
                        print(f"Added {entries_added} entries...")

        # Final commit for remaining entries
        db.session.commit()
        print(f"Successfully imported {entries_added} dictionary entries!")

if __name__ == '__main__':
    import_words()
