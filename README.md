# Genealogical Sources Management App

A web application for managing genealogical sources with a Flask backend, React frontend, and PostgreSQL database, all containerized with Docker.

## Project Status

🚧 Early development – scaffolded via [Cline](https://cline.tools) with backend/frontend structure in place. APIs and models are in progress.

## Features

- Manage genealogical sources (documents, records, photos, etc.)
- Organize sources by family members, events, or locations
- Search and filter sources
- User authentication
- Data export/import

## Planned Features

- OCR integration for scanned sources
- Source citation formats (e.g., Evidence Explained)
- GEDCOM import/export

_An ERD (Entity-Relationship Diagram) will be added once core models are finalized._

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## Project Structure

```
genealogy-app/
├── backend/                # Flask backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── config.py
│   │   └── database.py
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
├── docker-compose.yml
├── .env
└── README.md
```

## Setup

### Prerequisites

- Docker & Docker Compose (recommended for containerized setup)
- Python 3.8+
- Node.js 14+
- PostgreSQL (via Docker or local installation)

### Quick Start with Docker

1. Clone the repository
2. Set up environment variables in `.env` (see example below)
3. Run `docker-compose up -d` to start all services
4. Access the app at `http://localhost:3000`
5. (Optional) Run database migrations: `docker exec -it <backend_container> python migrate.py`

### Environment Variables

Create a `.env` file with:

```
# Database
POSTGRES_DB=genealogy_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Frontend
VITE_API_URL=http://localhost:5000/api
```

### Local Development (without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
# Initialize database (first time only)
flask db init
flask db migrate
flask db upgrade
python run.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Database Setup

For local PostgreSQL:
1. Install PostgreSQL
2. Create database: `createdb genealogy_db`
3. Update `.env` with your database credentials

### Database Schema

The app uses the following database tables:

- **sources**: Main table for genealogical sources (title, description, type, date, location)
- **users**: User authentication (future feature)
- **tags**: For categorizing sources
- **source_tags**: Many-to-many relationship between sources and tags

## API Endpoints

- `GET /api/sources` - List all sources
- `POST /api/sources` - Create new source
- `GET /api/sources/{id}` - Get source details
- `PUT /api/sources/{id}` - Update source
- `DELETE /api/sources/{id}` - Delete source
- `GET /api/tags` - List all tags
- `POST /api/tags` - Create new tag

## Features

- Create, read, update, and delete genealogical sources
- Organize sources by type (document, photo, record, etc.)
- Add tags and categories
- Search and filter functionality
- Responsive UI with React
- RESTful API with Flask

## Development Workflow

### With Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
# Initialize migrations (first time)
flask db init
flask db migrate
flask db upgrade
python run.py
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

### Database Migrations

To apply database migrations:
```bash
cd backend
python migrate.py
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Ensure PostgreSQL is running and credentials are correct in `.env`

2. **CORS Issues**: The backend includes CORS configuration, but ensure the frontend proxy is set up correctly

3. **Port Conflicts**: Check if ports 3000 (frontend) and 5000 (backend) are available

4. **Docker Issues**: Ensure Docker is running and you have sufficient permissions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

GenSource is released under a modified MIT License that permits use in professional and commercial work, but **prohibits resale or relicensing** of the software itself.

See the [LICENSE](./LICENSE) file for details.
