import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .enums import (
    ConfidenceLevel,
    ReliabilityStatus,
    EvidenceType,
    SupportsClaim
)
from .. import db
from .user import User
from .relationship import Relationship
from .individual import Fact


class SourceType(db.Model):
    __tablename__ = "source_types"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)  # e.g., 'birth_certificate'
    label = db.Column(db.String(128), nullable=False)            # e.g., 'Birth Certificate'
    description = db.Column(db.Text)                             # optional: explain its use
    is_active = db.Column(db.Boolean, default=True)

    sources = db.relationship("Source", back_populates="source_type")


class Source(db.Model):
    __tablename__ = "sources"

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    source_type_id = db.Column(db.Integer, db.ForeignKey("source_types.id"), nullable=False)
    file_path = db.Column(db.String)
    external_url = db.Column(db.String)
    source_text = db.Column(db.String)
    source_date = db.Column(db.Date)
    location = db.Column(db.String)
    confidence_level = db.Column(Enum(ConfidenceLevel))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    source_type = db.relationship("SourceType", back_populates="sources")
    created_by_user = db.relationship("User", backref="sources")

    # Methods
    def update_confidence_level(self, new_level, reason, user_id):
        if self.confidence_level != new_level:
            from .source import SourceReliabilityHistory
            history = SourceReliabilityHistory(
                source_id=self.id,
                reliability_status=new_level,
                reason=reason,
                changed_by_user_id=user_id
            )
            self.confidence_level = new_level
            db.session.add(history)

    def __repr__(self):
        return f"<Source {self.title} ({self.source_type.label})>"


class SourceReliabilityHistory(db.Model):
    __tablename__ = "source_reliability_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sources.id"), nullable=False)
    reliability_status = db.Column(Enum(ReliabilityStatus), nullable=False)
    reason = db.Column(db.Text)
    changed_at = db.Column(db.DateTime, server_default=db.func.now())
    changed_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    source = db.relationship("Source", backref="reliability_history")
    changed_by_user = db.relationship("User", backref="reliability_changes")

    def __repr__(self):
        return f"<ReliabilityChange {self.reliability_status.value} @ {self.changed_at}>"


class SourceCollection(db.Model):
    __tablename__ = "source_collections"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    parent_collection_id = db.Column(UUID(as_uuid=True), db.ForeignKey("source_collections.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    created_by_user = db.relationship("User", backref="created_collections")
    parent_collection = db.relationship("SourceCollection", remote_side=[id], backref="subcollections")

    def __repr__(self):
        return f"<SourceCollection {self.name}>"


class SourceCollectionItem(db.Model):
    __tablename__ = "source_collection_items"

    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sources.id"), primary_key=True)
    collection_id = db.Column(UUID(as_uuid=True), db.ForeignKey("source_collections.id"), primary_key=True)
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    added_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    source = db.relationship("Source", backref="collection_links")
    collection = db.relationship("SourceCollection", backref="source_links")
    added_by_user = db.relationship("User", backref="added_collection_items")

    def __repr__(self):
        return f"<SourceCollectionItem source={self.source_id} collection={self.collection_id}>"


class Citation(db.Model):
    __tablename__ = "citations"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cited_object_id = db.Column(UUID(as_uuid=True), nullable=False)
    cited_object_type = db.Column(db.String(50), nullable=False)  # "fact" or "relationship"
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sources.id"), nullable=False)
    evidence_type = db.Column(Enum(EvidenceType))
    source_notes = db.Column(db.Text)
    page_number = db.Column(db.Integer)
    section_reference = db.Column(db.String)
    supports_claim = db.Column(Enum(SupportsClaim))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    source = db.relationship("Source", backref="citations")
    created_by_user = db.relationship("User", backref="created_citations")

    @property
    def cited_object(self):
        if self.cited_object_type == "fact":
            return db.session.get(Fact, self.cited_object_id)
        elif self.cited_object_type == "relationship":
            return db.session.get(Relationship, self.cited_object_id)
        return None

    def __repr__(self):
        return f"<Citation {self.cited_object_type}={self.cited_object_id} source={self.source_id}>"
