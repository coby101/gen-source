from flask import request, jsonify, abort
from uuid import UUID
from app.models import (
    db, Source, SourceCollection, SourceCollectionItem, SourceReliabilityHistory
)
from . import api


# ------------------------------
# Helpers
# ------------------------------

def serialize_source(source):
    return {
        "id": str(source.id),
        "title": source.title,
        "description": source.description,
        "source_type": source.source_type.value if source.source_type else None,
        "file_path": source.file_path,
        "external_url": source.external_url,
        "citation_text": source.citation_text,
        "source_date": source.source_date.isoformat() if source.source_date else None,
        "location": source.location,
        "confidence_level": source.confidence_level.value if source.confidence_level else None,
        "notes": source.notes,
        "is_active": source.is_active,
        "created_at": source.created_at.isoformat() if source.created_at else None,
        "updated_at": source.updated_at.isoformat() if source.updated_at else None,
        "created_by_user_id": str(source.created_by_user_id),
    }

def serialize_history(entry):
    return {
        "id": str(entry.id),
        "source_id": str(entry.source_id),
        "reliability_status": entry.reliability_status.value,
        "reason": entry.reason,
        "changed_at": entry.changed_at.isoformat() if entry.changed_at else None,
        "changed_by_user_id": str(entry.changed_by_user_id)
    }

def serialize_collection(col):
    return {
        "id": str(col.id),
        "name": col.name,
        "description": col.description,
        "parent_collection_id": str(col.parent_collection_id) if col.parent_collection_id else None,
        "created_at": col.created_at.isoformat(),
        "created_by_user_id": str(col.created_by_user_id)
    }

def serialize_collection_item(item):
    return {
        "source_id": str(item.source_id),
        "collection_id": str(item.collection_id),
        "added_at": item.added_at.isoformat(),
        "added_by_user_id": str(item.added_by_user_id)
    }

# ------------------------------
# Source Routes
# ------------------------------

@api.route("/sources", methods=["GET"])
def get_sources():
    sources = Source.query.filter_by(is_active=True).all()
    return jsonify([serialize_source(s) for s in sources])


@api.route("/sources/<uuid:source_id>", methods=["GET"])
def get_source(source_id):
    source = Source.query.get_or_404(source_id)
    return jsonify(serialize_source(source))


@api.route("/sources", methods=["POST"])
def create_source():
    data = request.get_json()

    source = Source(
        title=data["title"],
        description=data.get("description"),
        source_type=data.get("source_type"),
        file_path=data.get("file_path"),
        external_url=data.get("external_url"),
        citation_text=data.get("citation_text"),
        source_date=data.get("source_date"),
        location=data.get("location"),
        confidence_level=data.get("confidence_level"),
        notes=data.get("notes"),
        is_active=True,
        created_by_user_id=data["created_by_user_id"],
    )
    db.session.add(source)
    db.session.commit()
    return jsonify(serialize_source(source)), 201


@api.route("/sources/<uuid:source_id>", methods=["PUT"])
def update_source(source_id):
    source = Source.query.get_or_404(source_id)
    data = request.get_json()

    if "confidence_level" in data:
        source.update_confidence_level(
            data["confidence_level"],
            reason=data.get("reason", ""),
            user_id=data.get("updated_by_user_id", source.created_by_user_id)
        )

    for field in [
        "title", "description", "source_type", "file_path", "external_url",
        "citation_text", "source_date", "location", "notes", "is_active"
    ]:
        if field in data:
            setattr(source, field, data[field])

    db.session.commit()
    return jsonify(serialize_source(source))


@api.route("/sources/<uuid:source_id>", methods=["DELETE"])
def delete_source(source_id):
    source = Source.query.get_or_404(source_id)
    source.is_active = False  # soft delete
    db.session.commit()
    return jsonify({"message": f"Source {source_id} marked as inactive."})


@api.route("/sources/<uuid:source_id>/reliability-history", methods=["GET"])
def get_source_reliability_history(source_id):
    source = Source.query.get_or_404(source_id)
    history = SourceReliabilityHistory.query.filter_by(source_id=source.id).order_by(SourceReliabilityHistory.changed_at.desc()).all()
    return jsonify([serialize_history(h) for h in history])


# ------------------------------
# Source Collection Routes
# ------------------------------

@api.route("/collections", methods=["GET"])
def get_collections():
    collections = SourceCollection.query.all()
    return jsonify([serialize_collection(c) for c in collections])


@api.route("/collections", methods=["POST"])
def create_collection():
    data = request.get_json()
    col = SourceCollection(
        name=data["name"],
        description=data.get("description"),
        parent_collection_id=data.get("parent_collection_id"),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(col)
    db.session.commit()
    return jsonify(serialize_collection(col)), 201


@api.route("/collections/<uuid:collection_id>/items", methods=["GET"])
def get_collection_items(collection_id):
    items = SourceCollectionItem.query.filter_by(collection_id=collection_id).all()
    return jsonify([serialize_collection_item(i) for i in items])


@api.route("/collections/<uuid:collection_id>/items", methods=["POST"])
def add_collection_item(collection_id):
    data = request.get_json()
    item = SourceCollectionItem(
        source_id=data["source_id"],
        collection_id=collection_id,
        added_by_user_id=data["added_by_user_id"]
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(serialize_collection_item(item)), 201
