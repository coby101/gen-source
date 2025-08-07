from flask import request, jsonify, abort
from uuid import UUID
from app.models import (
    db, Relationship, Citation, RelationshipQualifier
)
from . import api


# ------------------------------
# Helpers
# ------------------------------

def serialize_relationship(rel):
    return {
        "id": str(rel.id),
        "individual1_id": str(rel.individual1_id),
        "individual2_id": str(rel.individual2_id),
        "relationship_type": rel.relationship_type.value,
        "relationship_start_date": rel.relationship_start_date.isoformat() if rel.relationship_start_date else None,
        "relationship_end_date": rel.relationship_end_date.isoformat() if rel.relationship_end_date else None,
        "relationship_notes": rel.relationship_notes,
        "is_biological": rel.is_biological,
        "is_legal": rel.is_legal,
        "confidence_level": rel.confidence_level.value if rel.confidence_level else None,
        "created_at": rel.created_at.isoformat(),
        "updated_at": rel.updated_at.isoformat() if rel.updated_at else None,
        "created_by_user_id": str(rel.created_by_user_id)
    }

def serialize_citation(rs):
    return {
        "id": str(rs.id),
        "relationship_id": str(rs.relationship_id),
        "source_id": str(rs.source_id),
        "evidence_type": rs.evidence_type.value if rs.evidence_type else None,
        "source_notes": rs.source_notes,
        "page_number": rs.page_number,
        "section_reference": rs.section_reference,
        "supports_relationship": rs.supports_relationship.value if rs.supports_relationship else None,
        "created_at": rs.created_at.isoformat(),
        "created_by_user_id": str(rs.created_by_user_id)
    }

def serialize_qualifier(q):
    return {
        "id": str(q.id),
        "relationship_id": str(q.relationship_id),
        "qualifier": q.qualifier.value,
        "created_at": q.created_at.isoformat(),
        "created_by_user_id": str(q.created_by_user_id)
    }


# ------------------------------
# Relationship Routes
# ------------------------------

@api.route("/relationships", methods=["GET"])
def get_relationships():
    relationships = Relationship.query.all()
    return jsonify([serialize_relationship(r) for r in relationships])


@api.route("/relationships/<uuid:relationship_id>", methods=["GET"])
def get_relationship(relationship_id):
    rel = Relationship.query.get_or_404(relationship_id)
    return jsonify(serialize_relationship(rel))


@api.route("/relationships", methods=["POST"])
def create_relationship():
    data = request.get_json()
    rel = Relationship(
        individual1_id=data["individual1_id"],
        individual2_id=data["individual2_id"],
        relationship_type=data["relationship_type"],
        relationship_start_date=data.get("relationship_start_date"),
        relationship_end_date=data.get("relationship_end_date"),
        relationship_notes=data.get("relationship_notes"),
        is_biological=data.get("is_biological"),
        is_legal=data.get("is_legal"),
        confidence_level=data.get("confidence_level"),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(rel)
    db.session.commit()
    return jsonify(serialize_relationship(rel)), 201


@api.route("/relationships/<uuid:relationship_id>", methods=["PUT"])
def update_relationship(relationship_id):
    rel = Relationship.query.get_or_404(relationship_id)
    data = request.get_json()

    for field in [
        "relationship_type", "relationship_start_date", "relationship_end_date",
        "relationship_notes", "is_biological", "is_legal", "confidence_level"
    ]:
        if field in data:
            setattr(rel, field, data[field])

    db.session.commit()
    return jsonify(serialize_relationship(rel))


# ------------------------------
# Citation Routes
# ------------------------------

@api.route("/relationships/<uuid:relationship_id>/sources", methods=["GET"])
def get_citations(relationship_id):
    citations = Citation.query.filter_by(
        cited_object_type="relationship",
        cited_object_id=relationship_id).all()
    return jsonify([serialize_citation(c) for c in citations])


@api.route("/relationships/<uuid:relationship_id>/sources", methods=["POST"])
def add_relationship_citation(relationship_id):
    data = request.get_json()
    citation = Citation(
        cited_object_type="relationship",
        cited_object_id=relationship_id,
        source_id=data["source_id"],
        evidence_type=data.get("evidence_type"),
        source_notes=data.get("source_notes"),
        page_number=data.get("page_number"),
        section_reference=data.get("section_reference"),
        supports_claim=data.get("supports_relationship"),  # mapping to unified field
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(citation)
    db.session.commit()
    return jsonify(serialize_citation(citation)), 201

# ------------------------------
# Relationship Qualifier Routes
# ------------------------------

@api.route("/relationships/<uuid:relationship_id>/qualifiers", methods=["GET"])
def get_relationship_qualifiers(relationship_id):
    qualifiers = RelationshipQualifier.query.filter_by(relationship_id=relationship_id).all()
    return jsonify([serialize_qualifier(q) for q in qualifiers])


@api.route("/relationships/<uuid:relationship_id>/qualifiers", methods=["POST"])
def add_relationship_qualifier(relationship_id):
    data = request.get_json()
    q = RelationshipQualifier(
        relationship_id=relationship_id,
        qualifier=data["qualifier"],
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(q)
    db.session.commit()
    return jsonify(serialize_qualifier(q)), 201
