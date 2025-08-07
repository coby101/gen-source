from app import db
from app.models import SourceType

def seed_source_types():
    types = [
        ("birth_certificate", "Birth Certificate", "An official document recording a person's birth details."),
        ("death_certificate", "Death Certificate", "An official document stating the date, location, and cause of death."),
        ("marriage_certificate", "Marriage Certificate", "An official document confirming a marriage."),
        ("divorce_record", "Divorce Record", "A legal record of a dissolved marriage."),
        ("census_record", "Census Record", "A government enumeration of a population, often including family relationships and occupations."),
        ("military_record", "Military Record", "Documents related to military service, enlistment, or discharge."),
        ("immigration_record", "Immigration Record", "Documents showing arrival into a country, such as entry permits or landing records."),
        ("naturalization_record", "Naturalization Record", "Records of individuals becoming citizens."),
        ("passenger_list", "Passenger List", "A list of individuals arriving by ship or plane."),
        ("church_register", "Church Register", "Religious records of events like baptisms, marriages, and burials."),
        ("cemetery_record", "Cemetery Record", "Records of grave sites and burials."),
        ("obituary", "Obituary", "A published death notice with biographical information."),
        ("newspaper_article", "Newspaper Article", "News reports that may mention individuals or events."),
        ("photograph", "Photograph", "Visual documentation that can support identity or relationships."),
        ("personal_letter", "Personal Letter", "Correspondence that can reveal family connections or life events."),
        ("diary_or_journal", "Diary or Journal", "Personal records documenting daily life or reflections."),
        ("land_record", "Land Record", "Property transactions such as deeds or grants."),
        ("probate_record", "Probate Record", "Wills and estate settlements that often list heirs."),
        ("court_record", "Court Record", "Legal proceedings involving individuals."),
        ("school_record", "School Record", "Enrollment or academic history."),
        ("employment_record", "Employment Record", "Work history, including employers and roles."),
        ("voter_registration", "Voter Registration", "Records of eligible voters."),
        ("tax_record", "Tax Record", "Records of taxes paid or owed, which can show residency."),
        ("bible_record", "Bible Record", "Family events recorded in a family Bible."),
        ("family_tree", "Family Tree", "A compiled chart or list of familial relationships."),
        ("interview_or_oral_history", "Interview or Oral History", "Personal recollections recorded in audio or text."),
        ("government_id", "Government-issued ID", "Documents such as driver's licenses or passports."),
        ("online_tree", "Online Tree", "Family trees hosted on genealogy websites."),
        ("book", "Book", "Published works with relevant genealogical content."),
        ("article", "Article", "Published articles referencing people or events."),
        ("website", "Website", "Web-based sources containing genealogical data."),
        ("other", "Other", "A source that doesn't fit existing categories."),
    ]

    for key, label, description in types:
        existing = SourceType.query.filter_by(key=key).first()
        if not existing:
            db.session.add(SourceType(key=key, label=label, description=description))

    db.session.commit()
    