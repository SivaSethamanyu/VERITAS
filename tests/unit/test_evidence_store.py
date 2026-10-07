import pytest

from veritas.core.models import (
    Evidence,
    EvidenceType,
    Source,
)

from veritas.evidence.store import EvidenceStore


def test_add_and_get_source():
    store = EvidenceStore()

    source = Source(
        title="Example Source",
        source_type=EvidenceType.WEB,
        uri="https://example.com",
    )

    source_id = store.add_source(source)

    retrieved = store.get_source(source_id)

    assert retrieved is not None
    assert retrieved.id == source.id
    assert retrieved.title == "Example Source"


def test_add_and_get_evidence():
    store = EvidenceStore()

    source = Source(
        title="Example Dataset",
        source_type=EvidenceType.DATASET,
    )

    store.add_source(source)

    evidence = Evidence(
        source_id=source.id,
        content="Revenue decreased by 18%.",
        evidence_type=EvidenceType.DATASET,
        relevance_score=0.95,
        reliability_score=0.90,
    )

    evidence_id = store.add_evidence(evidence)

    retrieved = store.get_evidence(evidence_id)

    assert retrieved is not None
    assert retrieved.id == evidence.id
    assert retrieved.source_id == source.id


def test_evidence_requires_existing_source():
    store = EvidenceStore()

    fake_source_id = Source(
        title="Temporary",
        source_type=EvidenceType.WEB,
    ).id

    evidence = Evidence(
        source_id=fake_source_id,
        content="This should fail.",
        evidence_type=EvidenceType.WEB,
    )

    with pytest.raises(ValueError):
        store.add_evidence(evidence)


def test_get_evidence_for_source():
    store = EvidenceStore()

    source_a = Source(
        title="Source A",
        source_type=EvidenceType.WEB,
    )

    source_b = Source(
        title="Source B",
        source_type=EvidenceType.WEB,
    )

    store.add_source(source_a)
    store.add_source(source_b)

    evidence_a = Evidence(
        source_id=source_a.id,
        content="Evidence A",
        evidence_type=EvidenceType.WEB,
    )

    evidence_b = Evidence(
        source_id=source_b.id,
        content="Evidence B",
        evidence_type=EvidenceType.WEB,
    )

    store.add_evidence(evidence_a)
    store.add_evidence(evidence_b)

    result = store.get_evidence_for_source(source_a.id)

    assert len(result) == 1
    assert result[0].id == evidence_a.id