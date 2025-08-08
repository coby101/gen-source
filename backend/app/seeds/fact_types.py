from app.models.individual import FactType
from app import db

def seed_fact_types():
    types = [
        ("birth", "Birth", "Date and place a person was born."),
        ("death", "Death", "Date and place a person died."),
        ("marriage", "Marriage", "Marriage event between individuals."),
        ("divorce", "Divorce", "Legal dissolution of a marriage."),
        ("residence", "Residence", "Place where a person lived at a specific time."),
        ("occupation", "Occupation", "A person's job or profession."),
        ("education", "Education", "Schools attended or educational achievements."),
        ("military_service", "Military Service", "Participation in military organizations."),
        ("immigration", "Immigration", "Arrival into a new country."),
        ("emigration", "Emigration", "Departure from a country to live elsewhere."),
        ("naturalization", "Naturalization", "Acquiring citizenship in a new country."),
        ("religion", "Religion", "Religious affiliation or changes."),
        ("baptism", "Baptism", "Religious rite marking spiritual admission."),
        ("burial", "Burial", "Location and date of interment."),
        ("adoption", "Adoption", "Legal or informal adoption of a person."),
        ("name_change", "Name Change", "Legal or informal change of name."),
        ("event", "Event", "A general life event not covered by other types."),
        ("alias", "Alias", "Alternative name used by a person."),
        ("census", "Census", "Recorded presence in a population enumeration."),
        ("will", "Will", "Existence or content of a person's last will."),
        ("property", "Property", "Ownership or transfer of land or goods."),
        ("legal", "Legal", "Court or legal involvement."),
        ("medical", "Medical", "Medical conditions or health events."),
        ("travel", "Travel", "Significant journeys or trips."),
        ("honor", "Honor or Award", "Recognition such as medals or certificates."),
        ("photograph", "Photograph", "A specific instance of a photograph."),
        ("note", "Note", "An annotation or unstructured fact."),
        ("other", "Other", "A fact that doesn't fit predefined categories."),
    ]

    for key, label, description in types:
        existing = FactType.query.filter_by(key=key).first()
        if not existing:
            db.session.add(FactType(key=key, label=label, description=description))

    db.session.commit()
