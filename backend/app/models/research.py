import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from .. import db
from .user import User
from .individual import Individual, Fact
from .enums import NotePriority, NoteStatus, ResolutionStatus


# ===== MODELS =====

class ResearchNote(db.Model):
    __tablename__ = "research_notes"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    individual_id = db.Column(UUID(as_uuid=True), db.ForeignKey("individuals.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    priority = db.Column(Enum(NotePriority), default=NotePriority.medium)
    status = db.Column(Enum(NoteStatus), default=NoteStatus.todo)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    individual = db.relationship("Individual", backref="research_notes")
    created_by_user = db.relationship("User", backref="created_research_notes")

    def __repr__(self):
        return f"<ResearchNote {self.title}>"


class ConflictingFact(db.Model):
    __tablename__ = "conflicting_facts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fact1_id = db.Column(UUID(as_uuid=True), db.ForeignKey("facts.id"), nullable=False)
    fact2_id = db.Column(UUID(as_uuid=True), db.ForeignKey("facts.id"), nullable=False)
    conflict_description = db.Column(db.Text, nullable=False)

    resolution_status = db.Column(Enum(ResolutionStatus), default=ResolutionStatus.unresolved)
    resolution_notes = db.Column(db.Text)
    resolved_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    resolved_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    fact1 = db.relationship("Fact", foreign_keys=[fact1_id], backref="conflicts_as_fact1")
    fact2 = db.relationship("Fact", foreign_keys=[fact2_id], backref="conflicts_as_fact2")
    created_by_user = db.relationship("User", foreign_keys=[created_by_user_id], backref="created_conflicts")
    resolved_by_user = db.relationship("User", foreign_keys=[resolved_by_user_id], backref="resolved_conflicts")

    def __repr__(self):
        return f"<ConflictingFact {self.fact1_id} vs {self.fact2_id}>"
