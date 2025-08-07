from app.models.source import SourceType
from app import db

def seed_source_types():
    types = [
        ("birth_certificate", "Birth Certificate"),
        ("death_certificate", "Death Certificate"),
        ("marriage_certificate", "Marriage Certificate"),
        ("divorce_record", "Divorce Record"),
        ("census_record", "Census Record"),
        ("military_record", "Military Record"),
        ("immigration_record", "Immigration Record"),
        ("naturalization_record", "Naturalization Record"),
        ("passenger_list", "Passenger List"),
        ("church_register", "Church Register"),
        ("cemetery_record", "Cemetery Record"),
        ("obituary", "Obituary"),
        ("newspaper_article", "Newspaper Article"),
        ("photograph", "Photograph"),
        ("personal_letter", "Personal Letter"),
        ("diary_or_journal", "Diary or Journal"),
        ("land_record", "Land Record"),
        ("probate_record", "Probate Record"),
        ("court_record", "Court Record"),
        ("school_record", "School Record"),
        ("employment_record", "Employment Record"),
        ("voter_registration", "Voter Registration"),
        ("tax_record", "Tax Record"),
        ("bible_record", "Bible Record"),
        ("family_tree", "Family Tree"),
        ("interview_or_oral_history", "Interview or Oral History"),
        ("government_id", "Government-issued ID"),
        ("online_tree", "Online Tree"),
        ("book", "Book"),
        ("article", "Article"),
        ("website", "Website"),
        ("other", "Other"),
    ]

    for key, label in types:
        existing = SourceType.query.filter_by(key=key).first()
        if not existing:
            db.session.add(SourceType(key=key, label=label))

    db.session.commit()
