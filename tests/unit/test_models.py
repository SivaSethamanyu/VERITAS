from veritas.core.models import (
    Claim,
    ClaimStatus,
    Evidence,
    EvidenceType,
    Investigation,
    InvestigationQuestion,
    InvestigationStatus,
    Source,
)


def test_source_creation():
    source = Source(
        title="Example Source",
        source_type=EvidenceType.WEB,
        uri="https://example.com",
    )

    assert source.title == "Example Source"
    assert source.source_type == EvidenceType.WEB
    assert source.id is not None


def test_evidence_creation():
    source = Source(
        title="Example Dataset",
        source_type=EvidenceType.DATASET,
    )

    evidence = Evidence(
        source_id=source.id,
        content="Revenue decreased by 18%.",
        evidence_type=EvidenceType.DATASET,
        relevance_score=0.95,
        reliability_score=0.90,
    )

    assert evidence.source_id == source.id
    assert evidence.relevance_score == 0.95
    assert evidence.reliability_score == 0.90


def test_claim_creation():
    claim = Claim(
        statement="Revenue decreased significantly.",
        status=ClaimStatus.SUPPORTED,
        confidence=0.92,
    )

    assert claim.status == ClaimStatus.SUPPORTED
    assert claim.confidence == 0.92


def test_investigation_creation():
    question = InvestigationQuestion(
        text="Why did revenue decrease?"
    )

    investigation = Investigation(
        question=question
    )

    assert investigation.question.text == "Why did revenue decrease?"
    assert investigation.status == InvestigationStatus.CREATED