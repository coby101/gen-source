import enum

# ===== General Purpose Enums =====

class ConfidenceLevel(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    questionable = "questionable"
    certain = "certain"
    doubtful = "doubtful"
    speculative = "speculative"


class EvidenceType(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    circumstantial = "circumstantial"


class SupportsClaim(enum.Enum):  # Unified name for fact/relationship support
    supports = "supports"
    contradicts = "contradicts"
    neutral = "neutral"


class ReliabilityStatus(enum.Enum):
    reliable = "reliable"
    questionable = "questionable"
    unreliable = "unreliable"
    deprecated = "deprecated"


# ===== Domain-Specific Enums =====

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"


class RelationshipType(enum.Enum):
    parent = "parent"
    child = "child"
    spouse = "spouse"
    partner = "partner"
    sibling = "sibling"
    guardian = "guardian"
    ward = "ward"
    other = "other"


class Qualifier(enum.Enum):
    natural = "natural"
    adoptive = "adoptive"
    biological = "biological"
    step = "step"
    surrogate = "surrogate"
    legal = "legal"
    social = "social"
    genetic = "genetic"


class ExternalPlatform(enum.Enum):
    ancestry = "ancestry"
    myheritage = "myheritage"
    familysearch = "familysearch"
    findmypast = "findmypast"
    other = "other"


class NotePriority(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class NoteStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class ResolutionStatus(enum.Enum):
    unresolved = "unresolved"
    resolved = "resolved"
    dismissed = "dismissed"


__all__ = [
    "ConfidenceLevel",
    "EvidenceType",
    "SupportsClaim",
    "Gender",
    "RelationshipType",
    "ReliabilityStatus",
    "Qualifier",
    "ExternalPlatform",
    "NotePriority",
    "NoteStatus",
    "ResolutionStatus",
]
