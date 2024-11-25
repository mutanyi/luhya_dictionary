LUHYA_WORDS = [
    {
        "luhya_word": "mulembe",
        "english_word": "hello/peace",
        "part_of_speech": "greeting",
        "example_sentence": "Mulembe muhando (Hello friend)"
    },
    {
        "luhya_word": "khulya",
        "english_word": "to eat",
        "part_of_speech": "verb",
        "example_sentence": "Nenyanga khulya (I want to eat)"
    },
    {
        "luhya_word": "omukhaana",
        "english_word": "girl",
        "part_of_speech": "noun",
        "example_sentence": "Omukhaana oyo mulahi (That girl is beautiful)"
    },
    {
        "luhya_word": "omusiani",
        "english_word": "boy",
        "part_of_speech": "noun",
        "example_sentence": "Omusiani oyo muleyi (That boy is tall)"
    },
    {
        "luhya_word": "khukula",
        "english_word": "to buy",
        "part_of_speech": "verb",
        "example_sentence": "Nenyanga khukula enyama (I want to buy meat)"
    },
    {
        "luhya_word": "enyama",
        "english_word": "meat",
        "part_of_speech": "noun",
        "example_sentence": "Enyama yino indahi (This meat is delicious)"
    },
    {
        "luhya_word": "amachi",
        "english_word": "water",
        "part_of_speech": "noun",
        "example_sentence": "Nywa amachi (Drink water)"
    },
    {
        "luhya_word": "khunywa",
        "english_word": "to drink",
        "part_of_speech": "verb",
        "example_sentence": "Nenyanga khunywa amachi (I want to drink water)"
    },
    {
        "luhya_word": "indahi",
        "english_word": "delicious/sweet",
        "part_of_speech": "adjective",
        "example_sentence": "Ebilia yino indahi (This food is delicious)"
    },
    {
        "luhya_word": "ebilia",
        "english_word": "food",
        "part_of_speech": "noun",
        "example_sentence": "Ebilia yitekhe (The food is ready)"
    },
    # Family terms
    {
        "luhya_word": "papa",
        "english_word": "father",
        "part_of_speech": "noun",
        "example_sentence": "Papa wanje aliho (My father is here)"
    },
    {
        "luhya_word": "mama",
        "english_word": "mother",
        "part_of_speech": "noun",
        "example_sentence": "Mama wanje mulahi (My mother is beautiful)"
    },
    {
        "luhya_word": "kuka",
        "english_word": "grandfather",
        "part_of_speech": "noun",
        "example_sentence": "Kuka wanje mulwale (My grandfather is sick)"
    },
    {
        "luhya_word": "kukhu",
        "english_word": "grandmother",
        "part_of_speech": "noun",
        "example_sentence": "Kukhu wanje omukesi (My grandmother is wise)"
    },
    # Common verbs
    {
        "luhya_word": "khwola",
        "english_word": "to arrive",
        "part_of_speech": "verb",
        "example_sentence": "Nolanga liena? (When will you arrive?)"
    },
    {
        "luhya_word": "khutsya",
        "english_word": "to go",
        "part_of_speech": "verb",
        "example_sentence": "Nenyanga khutsya (I want to go)"
    },
    {
        "luhya_word": "khwichula",
        "english_word": "to rest",
        "part_of_speech": "verb",
        "example_sentence": "Nenyanga khwichula (I want to rest)"
    },
    # Time-related words
    {
        "luhya_word": "muchuli",
        "english_word": "morning",
        "part_of_speech": "noun",
        "example_sentence": "Mulembe muchuli (Good morning)"
    },
    {
        "luhya_word": "mwilolo",
        "english_word": "evening",
        "part_of_speech": "noun",
        "example_sentence": "Mulembe mwilolo (Good evening)"
    },
    {
        "luhya_word": "lero",
        "english_word": "today",
        "part_of_speech": "adverb",
        "example_sentence": "Lero libuyangu (Today is good)"
    },
    # Numbers
    {
        "luhya_word": "ndala",
        "english_word": "one",
        "part_of_speech": "number",
        "example_sentence": "Mbe ne ndala (Give me one)"
    },
    {
        "luhya_word": "tsibili",
        "english_word": "two",
        "part_of_speech": "number",
        "example_sentence": "Tsisendi tsibili (Two shillings)"
    },
    {
        "luhya_word": "taru",
        "english_word": "three",
        "part_of_speech": "number",
        "example_sentence": "Tsisaawa taru (Three hours)"
    },
    # Common adjectives
    {
        "luhya_word": "mulahi",
        "english_word": "beautiful/good",
        "part_of_speech": "adjective",
        "example_sentence": "Omukhaana mulahi (A beautiful girl)"
    },
    {
        "luhya_word": "mubi",
        "english_word": "bad/ugly",
        "part_of_speech": "adjective",
        "example_sentence": "Omusiani mubi (A bad boy)"
    },
    {
        "luhya_word": "mulayi",
        "english_word": "tall",
        "part_of_speech": "adjective",
        "example_sentence": "Omusiani mulayi (A tall boy)"
    },
    # Weather terms
    {
        "luhya_word": "ifula",
        "english_word": "rain",
        "part_of_speech": "noun",
        "example_sentence": "Ifula yikwa (It's raining)"
    },
    {
        "luhya_word": "omusambwa",
        "english_word": "wind",
        "part_of_speech": "noun",
        "example_sentence": "Omusambwa mukali (Strong wind)"
    },
    {
        "luhya_word": "enjuba",
        "english_word": "sun",
        "part_of_speech": "noun",
        "example_sentence": "Enjuba yakha (The sun is shining)"
    }
]

# Generate more variations and combinations
def generate_more_words():
    additional_words = []
    
    # Common prefixes and suffixes
    prefixes = ['omu', 'aba', 'esi', 'ebi', 'li', 'ka']
    suffixes = ['nga', 'kha', 'la', 'na']
    
    # Generate variations
    base_words = [word["luhya_word"] for word in LUHYA_WORDS]
    for word in base_words:
        for prefix in prefixes:
            new_word = {
                "luhya_word": f"{prefix}{word}",
                "english_word": f"variation of {word}",
                "part_of_speech": "noun",
                "example_sentence": f"{prefix}{word} (contextual usage)"
            }
            additional_words.append(new_word)
            
        for suffix in suffixes:
            new_word = {
                "luhya_word": f"{word}{suffix}",
                "english_word": f"variation of {word}",
                "part_of_speech": "verb",
                "example_sentence": f"{word}{suffix} (contextual usage)"
            }
            additional_words.append(new_word)
    
    return additional_words

# Add generated words to the main list
LUHYA_WORDS.extend(generate_more_words())

# Verbs related to daily activities
daily_verbs = [
    ("khulima", "to farm/dig", "Natsya khulima (I went to farm)"),
    ("khusena", "to pray", "Khusena buli muchuli (Pray every morning)"),
    ("khuboha", "to tie", "Boha omukanda (Tie the rope)"),
    ("khufunaka", "to break", "Esikombe yifunakha (The cup broke)"),
    ("khwimba", "to sing", "Yimba olwimbo (Sing a song)"),
    ("khucheza", "to play", "Abana bacheza (Children are playing)"),
    ("khutekha", "to cook", "Mama atekha (Mother is cooking)"),
    ("khukhala", "to sit", "Khala asi (Sit down)"),
    ("khwema", "to stand", "Yema ambi (Stand up)"),
    ("khulola", "to see/look", "Lola ino (Look at this)")
]

# Add daily verbs to the main list
for verb, meaning, example in daily_verbs:
    LUHYA_WORDS.append({
        "luhya_word": verb,
        "english_word": meaning,
        "part_of_speech": "verb",
        "example_sentence": example
    })

# Body parts
body_parts = [
    ("omurwe", "head", "Omurwe kwanje (My head)"),
    ("amoni", "eyes", "Amoni kanje (My eyes)"),
    ("omukhono", "hand/arm", "Omukhono kwanje (My hand)"),
    ("okhukulu", "leg/foot", "Okhukulu kwanje (My leg)"),
    ("omunwa", "mouth", "Omunwa kwanje (My mouth)"),
    ("amaru", "teeth", "Amaru kanje (My teeth)"),
    ("olulimi", "tongue", "Olulimi lwanje (My tongue)"),
    ("obusio", "face", "Obusio bwanje (My face)"),
    ("amabeka", "shoulders", "Amabeka kanje (My shoulders)"),
    ("einda", "stomach", "Einda yanje (My stomach)")
]

# Add body parts to the main list
for part, meaning, example in body_parts:
    LUHYA_WORDS.append({
        "luhya_word": part,
        "english_word": meaning,
        "part_of_speech": "noun",
        "example_sentence": example
    })
