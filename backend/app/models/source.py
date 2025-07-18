import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .. import db
from .user import User


class SourceType(enum.Enum):
    document = "document"
    image = "image"
    pdf = "pdf"
    citation = "citation"
    external_record = "external_record"


class ConfidenceLevel(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    questionable = "questionable"


class ReliabilityStatus(enum.Enum):
    reliable = "reliable"
    questionable = "questionable"
    unreliable = "unreliable"
    deprecated = "deprecated"


class Source(db.Model):
    __tablename__ = "sources"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    source_type = db.Column(Enum(SourceType), nullable=False)
    file_path = db.Column(db.String)
    external_url = db.Column(db.String)
    citation_text = db.Column(db.String)
    source_date = db.Column(db.Date)
    location = db.Column(db.String)
    confidence_level = db.Column(Enum(ConfidenceLevel))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    created_by_user = db.relationship("User", backref="sources")

    def __repr__(self):
        return f"<Source {self.title} ({self.source_type.value})>"


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
