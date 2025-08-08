# Enhanced Project Structure for Genealogical Source Management

## Recommended Directory Structure

```
GenSource/
├── README.md
├── LICENSE
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.example                    # Environment template
├── docs/                           # Documentation
│   ├── er_model_diagram.md         # Database design
│   ├── project_structure.md        # This file
│   ├── api_documentation.md        # API specs
│   ├── deployment_guide.md         # Deployment instructions
│   └── user_workflows.md           # User experience flows
├── scripts/                        # Development and deployment scripts
│   ├── setup_dev.sh               # Development environment setup
│   ├── backup_db.sh               # Database backup
│   ├── restore_db.sh              # Database restore
│   └── seed_data.py               # Sample data for development
├── docker/                         # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf                 # Production nginx config
├── backend/                        # Flask API server
│   ├── requirements.txt
│   ├── requirements-dev.txt        # Development dependencies
│   ├── run.py                     # Application entry point
│   ├── migrate.py                 # Database migration script
│   ├── app/                       # Main application package
│   │   ├── __init__.py            # App factory
│   │   ├── config.py              # Configuration settings
│   │   ├── models/                # Database models (organized by domain)
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base model with common fields
│   │   │   ├── user.py            # User model
│   │   │   ├── source.py          # Source-related models
│   │   │   ├── individual.py      # Individual and fact models
│   │   │   ├── relationship.py    # Relationship models
│   │   │   ├── audit.py           # Audit/history models
│   │   │   └── research.py        # Research notes and conflicts
│   │   ├── api/                   # API routes organized by domain
│   │   │   ├── __init__.py
│   │   │   ├── sources.py         # Source management endpoints
│   │   │   ├── individuals.py     # Individual management endpoints
│   │   │   ├── facts.py           # Fact management endpoints
│   │   │   ├── relationships.py   # Relationship endpoints
│   │   │   ├── research.py        # Research workflow endpoints
│   │   │   ├── external.py        # External system integration
│   │   │   └── reports.py         # Reporting and analysis endpoints
│   │   ├── services/              # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── source_service.py  # Source management logic
│   │   │   ├── fact_service.py    # Fact extraction and validation
│   │   │   ├── audit_service.py   # Change tracking and history
│   │   │   ├── conflict_service.py # Conflict detection and resolution
│   │   │   ├── external_sync.py   # External platform synchronization
│   │   │   └── file_service.py    # File upload and management
│   │   ├── utils/                 # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── validators.py      # Data validation utilities
│   │   │   ├── formatters.py      # Citation and date formatting
│   │   │   ├── file_handlers.py   # File processing (PDF, images)
│   │   │   ├── date_parser.py     # Genealogical date parsing
│   │   │   └── confidence.py      # Confidence level calculations
│   │   ├── auth/                  # Authentication and authorization
│   │   │   ├── __init__.py
│   │   │   ├── decorators.py      # Auth decorators
│   │   │   └── jwt_handler.py     # JWT token management
│   │   └── exceptions/            # Custom exceptions
│   │       ├── __init__.py
│   │       ├── source_exceptions.py
│   │       ├── validation_exceptions.py
│   │       └── auth_exceptions.py
│   ├── migrations/                # Database migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── tests/                     # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py           # Test configuration
│   │   ├── test_models/          # Model tests
│   │   ├── test_api/             # API endpoint tests
│   │   ├── test_services/        # Service layer tests
│   │   └── test_utils/           # Utility function tests
│   └── uploads/                   # File upload storage (development)
│       ├── sources/              # Source documents
│       ├── images/               # Image files
│       └── temp/                 # Temporary processing files
├── frontend/                      # React application
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   ├── index.html
│   ├── public/                   # Static assets
│   │   ├── vite.svg
│   │   └── favicon.ico
│   └── src/                      # React source code
│       ├── main.jsx              # Application entry point
│       ├── App.jsx               # Main App component
│       ├── App.css               # App-specific styles
│       ├── index.css             # Global styles
│       ├── assets/               # Static assets
│       ├── components/           # Reusable UI components
│       │   ├── common/           # Generic components
│       │   │   ├── Button.jsx
│       │   │   ├── Modal.jsx
│       │   │   ├── FileUpload.jsx
│       │   │   ├── DatePicker.jsx
│       │   │   └── ConfidenceIndicator.jsx
│       │   ├── sources/          # Source-related components
│       │   │   ├── SourceList.jsx
│       │   │   ├── SourceForm.jsx
│       │   │   ├── SourceDetail.jsx
│       │   │   ├── SourceViewer.jsx
│       │   │   └── SourceReliability.jsx
│       │   ├── individuals/      # Individual-related components
│       │   │   ├── IndividualList.jsx
│       │   │   ├── IndividualForm.jsx
│       │   │   ├── IndividualDetail.jsx
│       │   │   └── IndividualTimeline.jsx
│       │   ├── facts/            # Fact management components
│       │   │   ├── FactList.jsx
│       │   │   ├── FactForm.jsx
│       │   │   ├── FactDetail.jsx
│       │   │   └── FactConflicts.jsx
│       │   ├── relationships/    # Relationship components
│       │   │   ├── RelationshipDiagram.jsx
│       │   │   ├── RelationshipForm.jsx
│       │   │   └── FamilyTree.jsx
│       │   ├── research/         # Research workflow components
│       │   │   ├── ResearchNotes.jsx
│       │   │   ├── ConflictResolution.jsx
│       │   │   └── SourceAnalysis.jsx
│       │   └── reports/          # Reporting components
│       │       ├── IndividualReport.jsx
│       │       ├── SourceReport.jsx
│       │       └── AuditReport.jsx
│       ├── pages/                # Page-level components
│       │   ├── Dashboard.jsx
│       │   ├── SourceManagement.jsx
│       │   ├── IndividualManagement.jsx
│       │   ├── ResearchWorkspace.jsx
│       │   ├── Reports.jsx
│       │   └── Settings.jsx
│       ├── hooks/                # Custom React hooks
│       │   ├── useApi.js         # API interaction hook
│       │   ├── useAuth.js        # Authentication hook
│       │   ├── useFileUpload.js  # File upload hook
│       │   ├── useDebounce.js    # Debouncing hook
│       │   └── useLocalStorage.js # Local storage hook
│       ├── services/             # Frontend services
│       │   ├── api.js            # API client configuration
│       │   ├── sourceService.js  # Source API calls
│       │   ├── individualService.js # Individual API calls
│       │   ├── factService.js    # Fact API calls
│       │   ├── relationshipService.js # Relationship API calls
│       │   ├── authService.js    # Authentication service
│       │   └── fileService.js    # File handling service
│       ├── utils/                # Frontend utilities
│       │   ├── dateUtils.js      # Date formatting and parsing
│       │   ├── validators.js     # Form validation
│       │   ├── formatters.js     # Data formatting
│       │   ├── constants.js      # Application constants
│       │   └── helpers.js        # General helper functions
│       ├── context/              # React context providers
│       │   ├── AuthContext.jsx   # Authentication context
│       │   ├── ThemeContext.jsx  # UI theme context
│       │   └── NotificationContext.jsx # Notification system
│       ├── styles/               # Styling
│       │   ├── globals.css       # Global styles
│       │   ├── variables.css     # CSS variables
│       │   └── components/       # Component-specific styles
│       └── __tests__/            # Frontend tests
│           ├── components/       # Component tests
│           ├── pages/            # Page tests
│           ├── hooks/            # Hook tests
│           └── utils/            # Utility tests
└── storage/                      # Production file storage
    ├── sources/                  # Source documents
    ├── images/                   # Image files
    ├── backups/                  # Database backups
    └── exports/                  # Generated reports and exports
```

## Key Organizational Principles

### 1. Domain-Driven Structure
- Backend models, services, and API routes organized by domain (sources, individuals, facts, relationships)
- Frontend components grouped by functionality
- Clear separation of concerns between layers

### 2. Scalable Architecture
- Service layer for business logic separation
- Utility modules for reusable functionality
- Comprehensive testing structure
- Configuration management for different environments

### 3. Development Workflow Support
- Scripts for common development tasks
- Separate development and production requirements
- Test organization matching source structure
- Documentation co-located with code

### 4. File Management
- Organized upload storage by type
- Temporary processing areas
- Production storage separation
- Backup and export capabilities

### 5. Frontend Modularity
- Page-level components for routing
- Reusable component library
- Custom hooks for common functionality
- Service layer for API abstraction
- Context providers for global state

## Implementation Priority

### Phase 1: Core Infrastructure
1. Enhanced models (sources, individuals, facts)
2. Basic API endpoints
3. File upload service
4. Authentication system

### Phase 2: Source Management
1. Source upload and metadata
2. Fact extraction workflows
3. Source-fact linking
4. Basic conflict detection

### Phase 3: Research Workflows
1. Individual management
2. Relationship modeling
3. Research notes and tasks
4. Audit trail implementation

### Phase 4: Advanced Features
1. External system integration
2. Advanced conflict resolution
3. Reporting and analysis
4. Source reliability tracking

## Development Guidelines

### Backend
- Use SQLAlchemy models with proper relationships
- Implement service layer for business logic
- Add comprehensive error handling
- Include audit logging for all changes
- Use dependency injection for testability

### Frontend
- Follow React best practices with hooks
- Implement proper state management
- Use TypeScript for type safety (future enhancement)
- Include comprehensive error boundaries
- Implement responsive design patterns

### Testing
- Unit tests for all service functions
- Integration tests for API endpoints
- Component tests for React components
- End-to-end tests for critical workflows
- Mock external dependencies appropriately
