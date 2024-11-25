from app import app, db
from models import Dialect

def seed_dialects():
    """Seed the database with Luhya dialects and their information."""
    dialects_data = [
        {
            'name': 'Bukusu',
            'code': 'bukusu',
            'ethnic_group': 'Bukusu people',
            'regions': 'Bungoma, Mount Elgon district, and Trans Nzoia',
            'description': 'Spoken by the Bukusu people in Western Kenya.'
        },
        {
            'name': 'Lusamia',
            'code': 'lusamia',
            'ethnic_group': 'Samia people',
            'regions': 'Southern Region of Busia District',
            'description': 'Spoken by the Samia people in the Southern Region of Busia District.'
        },
        {
            'name': 'Lukhayo',
            'code': 'lukhayo',
            'ethnic_group': 'Khayo people',
            'regions': 'Nambale District and Matayos Division of Busia County',
            'description': 'Spoken by the Khayo people in Nambale District and Matayos Division.'
        },
        {
            'name': 'Lumarachi',
            'code': 'lumarachi',
            'ethnic_group': 'Marachi people',
            'regions': 'Butula District in Busia county',
            'description': 'Spoken by the Marachi people in Butula District.'
        },
        {
            'name': 'Lunyala',
            'code': 'lunyala',
            'ethnic_group': 'Nyala people',
            'regions': 'Busia District',
            'description': 'Spoken by the Nyala people in Busia District.'
        },
        {
            'name': 'LuKabarasi',
            'code': 'lukabarasi',
            'ethnic_group': 'Kabras people',
            'regions': 'Northern part of Kakamega district',
            'description': 'Spoken by the Kabras people in the northern part of Kakamega district.'
        },
        {
            'name': 'OluTsotso',
            'code': 'olutsotso',
            'ethnic_group': 'Tsotso people',
            'regions': 'Western part of Kakamega district',
            'description': 'Spoken by the Tsotso people in the western part of Kakamega district.'
        },
        {
            'name': 'Lwidakho',
            'code': 'lwidakho',
            'ethnic_group': 'Idakho people',
            'regions': 'Southern part of Kakamega district',
            'description': 'Spoken by the Idakho people in the southern part of Kakamega district.'
        },
        {
            'name': 'Lwisukha',
            'code': 'lwisukha',
            'ethnic_group': 'Isukha people',
            'regions': 'Eastern part of Kakamega district',
            'description': 'Spoken by the Isukha people in the eastern part of Kakamega district.'
        },
        {
            'name': 'Lulogooli',
            'code': 'lulogooli',
            'ethnic_group': 'Maragoli people',
            'regions': 'Vihiga district',
            'description': 'Spoken by the Maragoli people in Vihiga district.'
        },
        {
            'name': 'Olunyole',
            'code': 'olunyole',
            'ethnic_group': 'Nyole people',
            'regions': 'Bunyore in Vihiga district',
            'description': 'Spoken by the Nyole people in Bunyore, Vihiga district.'
        },
        {
            'name': 'Ludiliji',
            'code': 'ludiliji',
            'ethnic_group': 'Tiriki people',
            'regions': 'Tiriki in Vihiga district',
            'description': 'Spoken by the Tiriki people in Tiriki, Vihiga district.'
        },
        {
            'name': 'Oluwanga',
            'code': 'oluwanga',
            'ethnic_group': 'Wanga people',
            'regions': 'Mumias and Matungu Districts',
            'description': 'Spoken by the Wanga people in Mumias and Matungu Districts.'
        },
        {
            'name': 'OluShisa',
            'code': 'olushisa',
            'ethnic_group': 'Kisa people',
            'regions': 'Khwisero District',
            'description': 'Spoken by the Kisa people in Khwisero District.'
        },
        {
            'name': 'OluMarama',
            'code': 'olumarama',
            'ethnic_group': 'Marama people',
            'regions': 'Butere District',
            'description': 'Spoken by the Marama people in Butere District.'
        }
    ]

    with app.app_context():
        # Check if dialects already exist
        if Dialect.query.first() is not None:
            print("Dialects already seeded. Skipping...")
            return

        # Add all dialects
        for dialect_data in dialects_data:
            dialect = Dialect(**dialect_data)
            db.session.add(dialect)
        
        try:
            db.session.commit()
            print("Successfully seeded dialects!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding dialects: {e}")
            raise

if __name__ == '__main__':
    seed_dialects()
