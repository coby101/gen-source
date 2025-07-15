"""
Test configuration and fixtures for the genealogical source management system.
"""

import pytest
import tempfile
import os
from datetime import datetime
from app import create_app, db
from app.models import User, Source, Individual, Fact


@pytest.fixture
def app():
    """Create application for testing."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password',
            full_name='Test User'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_source(app, test_user):
    """Create a test source."""
    with app.app_context():
        source = Source(
            title='Test Birth Certificate',
            description='Birth certificate for John Doe',
            source_type='document',
            source_date=datetime(1950, 1, 1).date(),
            location='New York, NY',
            confidence_level='high',
            created_by_user_id=test_user.id
        )
        db.session.add(source)
        db.session.commit()
        return source


@pytest.fixture
def test_individual(app, test_user):
    """Create a test individual."""
    with app.app_context():
        individual = Individual(
            given_names='John',
            surname='Doe',
            preferred_name='John Doe',
            gender='male',
            birth_date_estimated=datetime(1950, 1, 1).date(),
            birth_place='New York, NY',
            created_by_user_id=test_user.id
        )
        db.session.add(individual)
        db.session.commit()
        return individual


@pytest.fixture
def test_fact(app, test_user, test_individual):
    """Create a test fact."""
    with app.app_context():
        fact = Fact(
            individual_id=test_individual.id,
            fact_type='birth',
            fact_value='Born in New York',
            fact_date=datetime(1950, 1, 1).date(),
            fact_place='New York, NY',
            confidence_level='high',
            is_primary=True,
            created_by_user_id=test_user.id
        )
        db.session.add(fact)
        db.session.commit()
        return fact


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for API requests."""
    # This would typically create a JWT token
    # For now, we'll use a simple approach
    return {
        'Authorization': f'Bearer test-token-{test_user.id}',
        'Content-Type': 'application/json'
    }


class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user(username='testuser', email='test@example.com'):
        """Create a test user."""
        return User(
            username=username,
            email=email,
            password_hash='hashed_password',
            full_name=f'Test {username.title()}'
        )
    
    @staticmethod
    def create_source(title='Test Source', user_id=None):
        """Create a test source."""
        return Source(
            title=title,
            description=f'Description for {title}',
            source_type='document',
            source_date=datetime(2000, 1, 1).date(),
            location='Test Location',
            confidence_level='medium',
            created_by_user_id=user_id
        )
    
    @staticmethod
    def create_individual(given_names='John', surname='Doe', user_id=None):
        """Create a test individual."""
        return Individual(
            given_names=given_names,
            surname=surname,
            preferred_name=f'{given_names} {surname}',
            gender='unknown',
            created_by_user_id=user_id
        )


@pytest.fixture
def data_factory():
    """Provide access to test data factory."""
    return TestDataFactory
