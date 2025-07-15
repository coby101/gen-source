"""
Base model with common fields and functionality for all models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from .. import db


class BaseModel(db.Model):
    """
    Base model class with common fields and methods.
    
    Provides:
    - UUID primary key
    - Created/updated timestamps
    - User attribution for changes
    - Soft deletion capability
    - Common utility methods
    """
    
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    @declared_attr
    def created_by_user_id(cls):
        return Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    @declared_attr
    def created_by_user(cls):
        return db.relationship('User', foreign_keys=[cls.created_by_user_id])
    
    def to_dict(self, include_relationships=False):
        """Convert model instance to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            else:
                result[column.name] = value
        
        if include_relationships:
            for relationship in self.__mapper__.relationships:
                if hasattr(self, relationship.key):
                    related_obj = getattr(self, relationship.key)
                    if related_obj is not None:
                        if hasattr(related_obj, 'to_dict'):
                            result[relationship.key] = related_obj.to_dict()
                        else:
                            result[relationship.key] = str(related_obj)
        
        return result
    
    def soft_delete(self):
        """Mark record as inactive instead of deleting."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def restore(self):
        """Restore a soft-deleted record."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_active(cls):
        """Get query for active records only."""
        return cls.query.filter(cls.is_active == True)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
