from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


# ============================================================
# ENUMS
# ============================================================


class InvestigationStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    INVESTIGATING = "investigating"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


class EvidenceType(str, Enum):
    WEB = "web"
    DOCUMENT = "document"
    DATASET = "dataset"
    DATABASE = "database"
    COMPUTATION = "computation"
    API = "api"
    OBSERVATION = "observation"


class ClaimStatus(str, Enum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    CONTRADICTED = "contradicted"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNKNOWN = "unknown"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskType(str, Enum):
    RETRIEVE = "retrieve"
    ANALYZE = "analyze"
    CALCULATE = "calculate"
    VERIFY = "verify"
    COMPARE = "compare"
    SYNTHESIZE = "synthesize"


# ============================================================
# BASE MODEL
# ============================================================


class VeritasBaseModel(BaseModel):
    """
    Base model used throughout VERITAS.

    extra='forbid' prevents accidental fields from silently
    entering the system.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )


# ============================================================
# SOURCE
# ============================================================


class Source(VeritasBaseModel):
    """
    Represents the origin of information used by VERITAS.
    """

    id: UUID = Field(default_factory=uuid4)

    title: str
    uri: str | None = None

    source_type: EvidenceType

    publisher: str | None = None
    author: str | None = None

    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = Field(default_factory=dict)


# ============================================================
# EVIDENCE
# ============================================================


class Evidence(VeritasBaseModel):
    """
    A specific piece of information obtained from a source.

    Evidence is the fundamental unit used to support or challenge
    claims inside VERITAS.
    """

    id: UUID = Field(default_factory=uuid4)

    source_id: UUID

    content: str

    evidence_type: EvidenceType

    relevance_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    reliability_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    location: str | None = None

    extracted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = Field(default_factory=dict)


# ============================================================
# CLAIM
# ============================================================


class Claim(VeritasBaseModel):
    """
    A proposition that can be supported, contradicted, or left
    unresolved by evidence.
    """

    id: UUID = Field(default_factory=uuid4)

    statement: str

    status: ClaimStatus = ClaimStatus.UNKNOWN

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    supporting_evidence: list[UUID] = Field(
        default_factory=list
    )

    contradicting_evidence: list[UUID] = Field(
        default_factory=list
    )

    assumptions: list[str] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ============================================================
# HYPOTHESIS
# ============================================================


class Hypothesis(VeritasBaseModel):
    """
    A possible explanation that VERITAS investigates.
    """

    id: UUID = Field(default_factory=uuid4)

    statement: str

    prior_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    posterior_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    supporting_evidence: list[UUID] = Field(
        default_factory=list
    )

    contradicting_evidence: list[UUID] = Field(
        default_factory=list
    )

    related_claims: list[UUID] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ============================================================
# TASK
# ============================================================


class InvestigationTask(VeritasBaseModel):
    """
    A concrete action that must be executed during an investigation.
    """

    id: UUID = Field(default_factory=uuid4)

    description: str

    task_type: TaskType

    status: TaskStatus = TaskStatus.PENDING

    depends_on: list[UUID] = Field(
        default_factory=list
    )

    result: Any | None = None

    error: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    completed_at: datetime | None = None


# ============================================================
# FINDING
# ============================================================


class Finding(VeritasBaseModel):
    """
    A verified conclusion produced from one or more claims.
    """

    id: UUID = Field(default_factory=uuid4)

    statement: str

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    supporting_claims: list[UUID] = Field(
        default_factory=list
    )

    contradicting_claims: list[UUID] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ============================================================
# INVESTIGATION QUESTION
# ============================================================


class InvestigationQuestion(VeritasBaseModel):
    """
    The original question submitted to VERITAS.
    """

    id: UUID = Field(default_factory=uuid4)

    text: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ============================================================
# INVESTIGATION
# ============================================================


class Investigation(VeritasBaseModel):
    """
    Complete state of a VERITAS investigation.
    """

    id: UUID = Field(default_factory=uuid4)

    question: InvestigationQuestion

    status: InvestigationStatus = InvestigationStatus.CREATED

    hypotheses: list[Hypothesis] = Field(
        default_factory=list
    )

    tasks: list[InvestigationTask] = Field(
        default_factory=list
    )

    sources: list[Source] = Field(
        default_factory=list
    )

    evidence: list[Evidence] = Field(
        default_factory=list
    )

    claims: list[Claim] = Field(
        default_factory=list
    )

    findings: list[Finding] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )