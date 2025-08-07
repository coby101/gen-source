from flask import request, jsonify, abort
from uuid import UUID
from app.models import (
    db, Individual, Fact, Citation, ExternalLink
)
from . import api


# ------------------------------
# Helpers
# ------------------------------

def serialize_individual(ind):
    return {
        "id": str(ind.id),
        "given_names": ind.given_names,
        "surname": ind.surname,
        "preferred_name": ind.preferred_name,
        "gender": ind.gender.value if ind.gender else None,
        "birth_date_estimated": ind.birth_date_estimated.isoformat() if ind.birth_date_estimated else None,
        "death_date_estimated": ind.death_date_estimated.isoformat() if ind.death_date_estimated else None,
        "birth_place": ind.birth_place,
        "death_place": ind.death_place,
        "notes": ind.notes,
        "is_living": ind.is_living,
        "created_at": ind.created_at.isoformat(),
        "updated_at": ind.updated_at.isoformat() if ind.updated_at else None,
        "created_by_user_id": str(ind.created_by_user_id)
    }

def serialize_fact(fact):
    return {
        "id": str(fact.id),
        "individual_id": str(fact.individual_id),
        "fact_type": fact.fact_type.value,
        "fact_value": fact.fact_value,
        "fact_date": fact.fact_date.isoformat() if fact.fact_date else None,
        "fact_place": fact.fact_place,
        "description": fact.description,
        "confidence_level": fact.confidence_level.value if fact.confidence_level else None,
        "is_primary": fact.is_primary,
        "created_at": fact.created_at.isoformat(),
        "updated_at": fact.updated_at.isoformat() if fact.updated_at else None,
        "created_by_user_id": str(fact.created_by_user_id)
    }

def serialize_external_link(link):
    return {
        "id": str(link.id),
        "individual_id": str(link.individual_id),
        "platform": link.platform.value,
        "external_id": link.external_id,
        "external_url": link.external_url,
        "sync_notes": link.sync_notes,
        "last_synced": link.last_synced.isoformat() if link.last_synced else None,
        "is_active": link.is_active,
        "created_at": link.created_at.isoformat(),
        "created_by_user_id": str(link.created_by_user_id)
    }


# ------------------------------
# Individual Routes
# ------------------------------

@api.route("/individuals", methods=["GET"])
def get_individuals():
    individuals = Individual.query.all()
    return jsonify([serialize_individual(i) for i in individuals])


@api.route("/individuals/<uuid:individual_id>", methods=["GET"])
def get_individual(individual_id):
    individual = Individual.query.get_or_404(individual_id)
    return jsonify(serialize_individual(individual))


@api.route("/individuals", methods=["POST"])
def create_individual():
    data = request.get_json()
    ind = Individual(
        given_names=data["given_names"],
        surname=data["surname"],
        preferred_name=data.get("preferred_name"),
        gender=data.get("gender"),
        birth_date_estimated=data.get("birth_date_estimated"),
        death_date_estimated=data.get("death_date_estimated"),
        birth_place=data.get("birth_place"),
        death_place=data.get("death_place"),
        notes=data.get("notes"),
        is_living=data.get("is_living", True),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(ind)
    db.session.commit()
    return jsonify(serialize_individual(ind)), 201


@api.route("/individuals/<uuid:individual_id>", methods=["PUT"])
def update_individual(individual_id):
    ind = Individual.query.get_or_404(individual_id)
    data = request.get_json()
    for field in [
        "given_names", "surname", "preferred_name", "gender",
        "birth_date_estimated", "death_date_estimated",
        "birth_place", "death_place", "notes", "is_living"
    ]:
        if field in data:
            setattr(ind, field, data[field])
    db.session.commit()
    return jsonify(serialize_individual(ind))


@api.route("/individuals/<uuid:individual_id>/facts", methods=["GET"])
def get_facts(individual_id):
    facts = Fact.query.filter_by(individual_id=individual_id).all()
    return jsonify([serialize_fact(f) for f in facts])


@api.route("/individuals/<uuid:individual_id>/facts", methods=["POST"])
def create_fact(individual_id):
    data = request.get_json()
    fact = Fact(
        individual_id=individual_id,
        fact_type=data["fact_type"],
        fact_value=data.get("fact_value"),
        fact_date=data.get("fact_date"),
        fact_place=data.get("fact_place"),
        description=data.get("description"),
        confidence_level=data.get("confidence_level"),
        is_primary=data.get("is_primary", False),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(fact)
    db.session.commit()
    return jsonify(serialize_fact(fact)), 201


@api.route("/facts/<uuid:fact_id>/sources", methods=["GET"])
def get_citations(fact_id):
    sources = Citation.query.filter_by(fact_id=fact_id).all()
    return jsonify([serialize_citation(s) for s in sources])


@api.route("/facts/<uuid:fact_id>/sources", methods=["POST"])
def add_fact_citation(fact_id):
    data = request.get_json()
    link = Citation(
        fact_id=fact_id,
        source_id=data["source_id"],
        evidence_type=data.get("evidence_type"),
        source_notes=data.get("source_notes"),
        page_number=data.get("page_number"),
        section_reference=data.get("section_reference"),
        supports_claim=data.get("supports_claim"),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(link)
    db.session.commit()
    return jsonify(serialize_citation(link)), 201


@api.route("/individuals/<uuid:individual_id>/links", methods=["GET"])
def get_external_links(individual_id):
    links = ExternalLink.query.filter_by(individual_id=individual_id).all()
    return jsonify([serialize_external_link(l) for l in links])


@api.route("/individuals/<uuid:individual_id>/links", methods=["POST"])
def create_external_link(individual_id):
    data = request.get_json()
    link = ExternalLink(
        individual_id=individual_id,
        platform=data["platform"],
        external_id=data["external_id"],
        external_url=data.get("external_url"),
        sync_notes=data.get("sync_notes"),
        last_synced=data.get("last_synced"),
        is_active=data.get("is_active", True),
        created_by_user_id=data["created_by_user_id"]
    )
    db.session.add(link)
    db.session.commit()
    return jsonify(serialize_external_link(link)), 201
