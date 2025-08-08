import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .enums import (
    ConfidenceLevel,
    Gender,
    ExternalPlatform,
)
from .. import db
from .user import User


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


class FactType(db.Model):
    __tablename__ = "fact_types"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)  # e.g., 'birth_certificate'
    label = db.Column(db.String(128), nullable=False)            # e.g., 'Birth Certificate'
    description = db.Column(db.Text)                             # optional: explain its use

    facts = db.relationship("Fact", back_populates="fact_type")

    def __repr__(self):
        return f"<FactType {self.name}>"


class Fact(db.Model):
    __tablename__ = "facts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    individual_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    fact_type_id = db.Column(db.Integer, db.ForeignKey("fact_types.id"), nullable=False)
    fact_type = db.relationship("FactType", back_populates="facts")
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
        return f"<Fact {self.fact_type.name} for Individual {self.individual_id}>"


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
