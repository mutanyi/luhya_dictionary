# Luhya Language Dictionary

A comprehensive web-based bilingual dictionary application for the Luhya language, focusing on academic verification and cultural preservation.

## Features

- Bilingual dictionary (Luhya-English)
- Multiple dialect support (currently focusing on Luwanga)
- User authentication with role-based access
- Academic verification system
- Comprehensive word entries including:
  - Part of speech
  - Usage examples
  - Cultural notes
  - Dialectal variations
  - Source attribution

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd luhya_dictionary
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python src/seed_database.py
```

5. Run the application:
```bash
python src/app.py
```

The application will be available at http://localhost:5000

## User Roles

1. **Admin**
   - Verify language experts
   - Approve dictionary entries
   - Manage user roles

2. **Verified Language Expert**
   - Add new words
   - Edit existing entries
   - Provide cultural context

3. **Unverified User**
   - Browse dictionary
   - Search words
   - Register as language expert

## Project Structure

```
luhya_dictionary/
├── documents/                # Documentation and source files
│   └── Luhya_words.txt      # Source dictionary data
├── src/                     # Source code
│   ├── app.py              # Main application file
│   ├── models.py           # Database models
│   ├── forms.py            # Form definitions
│   ├── database.py         # Database configuration
│   └── templates/          # HTML templates
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on Appleby's 1943 Luhya-English Vocabulary
- Luwanga dialect translations by Alfred Anangwe (2006)
- Electronic version preparation by Michael Marlo with assistance from University of Michigan students
