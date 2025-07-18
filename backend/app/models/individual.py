import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .. import db
from .user import User
from .source import Source


# ===== ENUMS =====

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"


class FactType(enum.Enum):
    birth = "birth"
    death = "death"
    marriage = "marriage"
    divorce = "divorce"
    residence = "residence"
    occupation = "occupation"
    education = "education"
    military = "military"
    immigration = "immigration"
    other = "other"


class ConfidenceLevel(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    questionable = "questionable"


class EvidenceType(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    circumstantial = "circumstantial"


class SupportsFact(enum.Enum):
    supports = "supports"
    contradicts = "contradicts"
    neutral = "neutral"


class ExternalPlatform(enum.Enum):
    ancestry = "ancestry"
    myheritage = "myheritage"
    familysearch = "familysearch"
    findmypast = "findmypast"
    other = "other"


# ===== MODELS =====

class Individual(db.Model):
    __tablename__ = "individuals"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    given_names = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    preferred_name = db.Column(db.String(255))
    gender = db.Column(Enum(Gender), nullable=False, default=Gender.unknown)

    birth_date_estimated = db.Column(db.Date)
    death_date_estimated = db.Column(db.Date)
    birth_place = db.Column(db.String(255))
    death_place = db.Column(db.String(255))
    notes = db.Column(db.Text)
    is_living = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    created_by_user = db.relationship("User", backref="created_individuals")

    def __repr__(self):
        return f"<Individual {self.preferred_name or (self.given_names + ' ' + self.surname)}>"


class Fact(db.Model):
    __tablename__ = "facts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    individual_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    fact_type = db.Column(Enum(FactType), nullable=False)
    fact_value = db.Column(db.String)
    fact_date = db.Column(db.Date)
    fact_place = db.Column(db.String)
    description = db.Column(db.Text)
    confidence_level = db.Column(Enum(ConfidenceLevel))
    is_primary = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    individual = db.relationship("Individual", backref="facts")
    created_by_user = db.relationship("User", backref="created_facts")

    def __repr__(self):
        return f"<Fact {self.fact_type.value} for Individual {self.individual_id}>"


class FactSource(db.Model):
    __tablename__ = "fact_sources"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fact_id = db.Column(UUID(as_uuid=True), db.ForeignKey("facts.id"), nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sources.id"), nullable=False)
    evidence_type = db.Column(Enum(EvidenceType))
    source_notes = db.Column(db.Text)
    page_number = db.Column(db.Integer)
    section_reference = db.Column(db.String)
    supports_fact = db.Column(Enum(SupportsFact))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    fact = db.relationship("Fact", backref="sources")
    source = db.relationship("Source", backref="fact_links")
    created_by_user = db.relationship("User", backref="created_fact_sources")

    def __repr__(self):
        return f"<FactSource fact={self.fact_id} source={self.source_id}>"


class ExternalLink(db.Model):
    __tablename__ = "external_links"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    individual_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    platform = db.Column(Enum(ExternalPlatform), nullable=False)
    external_id = db.Column(db.String, nullable=False)
    external_url = db.Column(db.String)
    sync_notes = db.Column(db.Text)
    last_synced = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    individual = db.relationship("Individual", backref="external_links")
    created_by_user = db.relationship("User", backref="external_links_created")

    def __repr__(self):
        return f"<ExternalLink {self.platform.value}:{self.external_id}>"
