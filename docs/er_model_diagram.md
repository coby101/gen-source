# Genealogical Source Management - Entity Relationship Model

## Core Design Principles
1. **Source-Centric**: All facts must be traceable to sources
2. **Auditability**: Complete history of data changes and source reliability
3. **Flexible Relationships**: Support for non-traditional family structures
4. **External Integration**: Links to records in other genealogy platforms

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Core Entities
    SOURCES {
        uuid id PK
        string title
        text description
        enum source_type
        string file_path
        string external_url
        string source_text
        date source_date
        string location
        enum confidence_level
        text notes
        string acquired_from
        date acquisition_date
        text provenance_notes
        boolean is_active
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    INDIVIDUALS {
        uuid id PK
        string given_names
        string surname
        string preferred_name
        enum gender "male|female|other|unknown"
        date birth_date_estimated
        date death_date_estimated
        string birth_place
        string death_place
        text notes
        boolean is_living
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    FACTS {
        uuid id PK
        uuid individual_id FK
        enum fact_type
        string fact_value
        date fact_date
        string fact_place
        text description
        enum confidence_level
        boolean is_primary
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    RELATIONSHIPS {
        uuid id PK
        uuid individual1_id FK
        uuid individual2_id FK
        enum relationship_type
        date relationship_start_date
        date relationship_end_date
        string relationship_notes
        boolean is_biological
        boolean is_legal
        enum confidence_level
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    RELATIONSHIP_QUALIFIERS {
        uuid id PK
        uuid relationship_id FK
        enum qualifier "adoptive|biological|step|surrogate|legal|social|genetic"
        timestamp created_at
        uuid created_by_user_id FK
    }

    %% Source Attribution and Evidence
    CITATIONS {
        uuid id PK
        uuid source_id FK
        string cited_object_type "fact or relationship"
        uuid cited_object_id
        integer page_number
        string section_reference
        text quote
        enum confidence_level_override
        enum supports "supports|contradicts|neutral"
        enum legibility "clear|faint|illegible"
        text interpretation_notes
        boolean private
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    %% External System Integration
    EXTERNAL_LINKS {
        uuid id PK
        uuid individual_id FK
        enum platform "ancestry|myheritage|familysearch|findmypast|other"
        string external_id "ID in external system"
        string external_url
        text sync_notes
        timestamp last_synced
        boolean is_active
        timestamp created_at
        uuid created_by_user_id FK
    }

    %% Source Management and Reliability
    SOURCE_RELIABILITY_HISTORY {
        uuid id PK
        uuid source_id FK
        enum reliability_status "reliable|questionable|unreliable|deprecated"
        text reason "why reliability changed"
        timestamp changed_at
        uuid changed_by_user_id FK
    }

    SOURCE_COLLECTIONS {
        uuid id PK
        string name
        text description
        uuid parent_collection_id FK "for hierarchical collections"
        timestamp created_at
        uuid created_by_user_id FK
    }

    SOURCE_COLLECTION_ITEMS {
        uuid source_id FK
        uuid collection_id FK
        timestamp added_at
        uuid added_by_user_id FK
    }

    %% User Management
    USERS {
        uuid id PK
        string username
        string email
        string password_hash
        string full_name
        boolean is_active
        timestamp created_at
        timestamp last_login
    }

    %% Research and Analysis
    RESEARCH_NOTES {
        uuid id PK
        uuid individual_id FK
        string title
        text content
        enum priority "high|medium|low"
        enum status "todo|in_progress|completed|blocked"
        timestamp created_at
        timestamp updated_at
        uuid created_by_user_id FK
    }

    CONFLICTING_FACTS {
        uuid id PK
        uuid fact1_id FK
        uuid fact2_id FK
        text conflict_description
        enum resolution_status "unresolved|resolved|dismissed"
        text resolution_notes
        uuid resolved_by_user_id FK
        timestamp resolved_at
        timestamp created_at
        uuid created_by_user_id FK
    }

    %% Relationships
    SOURCES ||--o{ CITATIONS : "is cited by"
    SOURCES ||--o{ SOURCE_RELIABILITY_HISTORY : "has_history"
    SOURCES ||--o{ SOURCE_COLLECTION_ITEMS : "belongs_to"
    
    INDIVIDUALS ||--o{ FACTS : "has"
    INDIVIDUALS ||--o{ EXTERNAL_LINKS : "linked_to"
    INDIVIDUALS ||--o{ RESEARCH_NOTES : "has"
    INDIVIDUALS ||--o{ RELATIONSHIPS : "individual1"
    INDIVIDUALS ||--o{ RELATIONSHIPS : "individual2"
    
    CITATIONS }o--|| FACTS : "supports"
    CITATIONS }o--|| RELATIONSHIPS : "supports"
    FACTS ||--o{ CONFLICTING_FACTS : "fact1"
    FACTS ||--o{ CONFLICTING_FACTS : "fact2"
    
    RELATIONSHIPS ||--o{ RELATIONSHIP_QUALIFIERS : "qualified_by"
    
    SOURCE_COLLECTIONS ||--o{ SOURCE_COLLECTION_ITEMS : "contains"
    SOURCE_COLLECTIONS ||--o{ SOURCE_COLLECTIONS : "parent"
    
    USERS ||--o{ SOURCES : "created"
    USERS ||--o{ INDIVIDUALS : "created"
    USERS ||--o{ FACTS : "created"
    USERS ||--o{ RELATIONSHIPS : "created"
    USERS ||--o{ RESEARCH_NOTES : "created"
    USERS ||--o{ SOURCE_RELIABILITY_HISTORY : "changed"
```

## Key Design Features

### 1. Source-Centric Architecture
- Every fact and relationship must be linked to at least one source
- Sources can support, contradict, or be neutral toward facts
- Multiple sources can support the same fact with different evidence types

### 2. Comprehensive Auditability
- Complete change history for individuals and facts
- Source reliability tracking with historical changes
- User attribution for all changes and additions

### 3. Flexible Relationship Model
- Supports biological, legal, adoptive, step, and guardian relationships
- Handles non-traditional family structures
- Relationship start/end dates for complex family dynamics

### 4. External System Integration
- Links to records in Ancestry, MyHeritage, FamilySearch, etc.
- Sync tracking and status management
- Maintains independence while enabling cross-referencing

### 5. Research Workflow Support
- Research notes and task management
- Conflict detection and resolution tracking
- Source collections for organization

### 6. Data Quality Management
- Confidence levels for sources, facts, and relationships
- Primary vs alternative facts
- Soft deletion with is_active flags
- Conflicting facts identification and resolution

## Usage Patterns

### Adding a Source with Facts
1. Upload/create source record
2. Link individuals mentioned in source
3. Extract facts from source
4. Create citations links with evidence assessment
5. Note any conflicts with existing facts

### Deprecating Unreliable Sources
1. Update source reliability status
2. System flags all facts supported only by deprecated sources
3. User can review and find alternative sources or mark facts as questionable
4. Complete audit trail maintained

### Research Workflow
1. Identify research goals via research_notes
2. Find and evaluate sources
3. Extract and link facts
4. Resolve conflicts between sources
5. Track confidence levels and evidence quality
