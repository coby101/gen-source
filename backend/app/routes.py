from flask import Blueprint, request, jsonify
from . import db
from datetime import datetime
from .models import (
    Source, SourceReliabilityHistory, SourceCollection, SourceCollectionItem,
    User, Individual, Fact, Citation, ExternalLink,
    Relationship, RelationshipQualifier,
    ResearchNote, ConflictingFact
)

main = Blueprint('main', __name__)

@main.route('/api/sources', methods=['GET'])
def get_sources():
    sources = Source.query.all()
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'description': s.description,
        'source_type': s.source_type,
        'date': s.date.isoformat() if s.date else None,
        'location': s.location,
        'created_at': s.created_at.isoformat()
    } for s in sources])

@main.route('/api/sources', methods=['POST'])
def create_source():
    data = request.get_json()
    
    new_source = Source(
        title=data.get('title'),
        description=data.get('description'),
        source_type=data.get('source_type'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else None,
        location=data.get('location')
    )
    
    db.session.add(new_source)
    db.session.commit()
    
    return jsonify({
        'id': new_source.id,
        'title': new_source.title,
        'description': new_source.description,
        'source_type': new_source.source_type,
        'date': new_source.date.isoformat() if new_source.date else None,
        'location': new_source.location,
        'created_at': new_source.created_at.isoformat()
    }), 201

@main.route('/api/sources/<int:id>', methods=['GET'])
def get_source(id):
    source = Source.query.get_or_404(id)
    return jsonify({
        'id': source.id,
        'title': source.title,
        'description': source.description,
        'source_type': source.source_type,
        'date': source.date.isoformat() if source.date else None,
        'location': source.location,
        'created_at': source.created_at.isoformat()
    })

@main.route('/api/sources/<int:id>', methods=['PUT'])
def update_source(id):
    source = Source.query.get_or_404(id)
    data = request.get_json()
    
    source.title = data.get('title', source.title)
    source.description = data.get('description', source.description)
    source.source_type = data.get('source_type', source.source_type)
    source.date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else source.date
    source.location = data.get('location', source.location)
    
    db.session.commit()
    
    return jsonify({
        'id': source.id,
        'title': source.title,
        'description': source.description,
        'source_type': source.source_type,
        'date': source.date.isoformat() if source.date else None,
        'location': source.location
    })

@main.route('/api/sources/<int:id>', methods=['DELETE'])
def delete_source(id):
    source = Source.query.get_or_404(id)
    db.session.delete(source)
    db.session.commit()
    return '', 204
