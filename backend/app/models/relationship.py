import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .. import db
from .user import User
from .individual import Individual
from .source import Source


# ===== ENUMS =====

class RelationshipType(enum.Enum):
    parent = "parent"
    child = "child"
    spouse = "spouse"
    partner = "partner"
    sibling = "sibling"
    guardian = "guardian"
    ward = "ward"
    other = "other"


class ConfidenceLevel(enum.Enum):
    certain = "certain"
    high = "high"
    medium = "medium"
    low = "low"
    doubtful = "doubtful"
    speculative = "speculative"


class EvidenceType(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    circumstantial = "circumstantial"


class SupportsRelationship(enum.Enum):
    supports = "supports"
    contradicts = "contradicts"
    neutral = "neutral"


class Qualifier(enum.Enum):
    natural = "natural"
    adoptive = "adoptive"
    biological = "biological"
    step = "step"
    surrogate = "surrogate"
    legal = "legal"
    social = "social"
    genetic = "genetic"


# ===== MODELS =====

class Relationship(db.Model):
    __tablename__ = "relationships"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    individual1_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    individual2_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    relationship_type = db.Column(Enum(RelationshipType), nullable=False)
    relationship_start_date = db.Column(db.Date)
    relationship_end_date = db.Column(db.Date)
    relationship_notes = db.Column(db.String)
    confidence_level = db.Column(Enum(ConfidenceLevel))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    individual1 = db.relationship("Individual", foreign_keys=[individual1_id], backref="relationships_as_1")
    individual2 = db.relationship("Individual", foreign_keys=[individual2_id], backref="relationships_as_2")
    created_by_user = db.relationship("User", backref="created_relationships")

    def __repr__(self):
        return f"<Relationship {self.relationship_type.value} between {self.individual1_id} and {self.individual2_id}>"


class RelationshipSource(db.Model):
    __tablename__ = "relationship_sources"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id = db.Column(UUID(as_uuid=True), db.ForeignKey("relationships.id"), nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sources.id"), nullable=False)
    evidence_type = db.Column(Enum(EvidenceType))
    source_notes = db.Column(db.Text)
    page_number = db.Column(db.Integer)
    section_reference = db.Column(db.String)
    supports_relationship = db.Column(Enum(SupportsRelationship))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    relationship = db.relationship("Relationship", backref="sources")
    source = db.relationship("Source", backref="relationship_links")
    created_by_user = db.relationship("User", backref="created_relationship_sources")

    def __repr__(self):
        return f"<RelationshipSource rel={self.relationship_id} src={self.source_id}>"


class RelationshipQualifier(db.Model):
    __tablename__ = "relationship_qualifiers"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id = db.Column(UUID(as_uuid=True), db.ForeignKey("relationships.id"), nullable=False)
    qualifier = db.Column(Enum(Qualifier), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    relationship = db.relationship("Relationship", backref="qualifiers")
    created_by_user = db.relationship("User", backref="created_relationship_qualifiers")

    def __repr__(self):
        return f"<RelationshipQualifier {self.qualifier.value} for {self.relationship_id}>"
