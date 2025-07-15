#!/bin/bash

# Development Environment Setup Script for GenSource
# This script sets up the development environment for the genealogical source management tool

set -e  # Exit on any error

echo "🚀 Setting up GenSource development environment..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the GenSource root directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your specific configuration"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p backend/uploads/{sources,images,temp}
mkdir -p storage/{sources,images,backups,exports}
mkdir -p backend/tests/{test_models,test_api,test_services,test_utils}
mkdir -p frontend/src/__tests__/{components,pages,hooks,utils}

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Initialize database
echo "🗄️  Setting up database..."
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions)" ]; then
    echo "Creating initial database migration..."
    flask db init || true  # Don't fail if already initialized
    flask db migrate -m "Initial migration with enhanced models"
fi

echo "Applying database migrations..."
flask db upgrade

cd ..

# Frontend setup
echo "⚛️  Setting up React frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

# Docker setup
echo "🐳 Setting up Docker environment..."
docker-compose build

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Start the development environment:"
echo "   docker-compose up"
echo "3. Or run services individually:"
echo "   Backend: cd backend && source venv/bin/activate && flask run"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "📚 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   Database: localhost:5432"
