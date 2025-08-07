"""
Database models for the genealogical source management system.

This package contains all SQLAlchemy models organized by domain:
- base: Base model with common fields
- user: User authentication and management
- source: Source documents and metadata
- individual: Individual records and facts
- relationship: Family relationships
- audit: Change tracking and history
- research: Research notes and conflict resolution
"""

from .base import BaseModel
from .user import User
from .source import Source, SourceReliabilityHistory, SourceCollection, SourceCollectionItem
from .individual import Individual, Fact, Citation, ExternalLink
from .relationship import Relationship, RelationshipQualifier
from .research import ResearchNote, ConflictingFact

__all__ = [
    'BaseModel',
    'User',
    'Source',
    'SourceReliabilityHistory', 
    'SourceCollection',
    'SourceCollectionItem',
    'Individual',
    'Fact',
    'Citation',
    'ExternalLink',
    'Relationship',
    'ResearchNote',
    'ConflictingFact'
]
