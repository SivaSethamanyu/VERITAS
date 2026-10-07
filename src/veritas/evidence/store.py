from uuid import UUID

from veritas.core.models import Evidence, Source


class EvidenceStore:
    """
    In-memory evidence and source registry.

    This is the first implementation of the VERITAS evidence layer.
    Later this interface can be backed by PostgreSQL or another
    persistent storage system without changing the rest of VERITAS.
    """

    def __init__(self) -> None:
        self._sources: dict[UUID, Source] = {}
        self._evidence: dict[UUID, Evidence] = {}

    # ---------------------------------------------------------
    # SOURCE OPERATIONS
    # ---------------------------------------------------------

    def add_source(self, source: Source) -> UUID:
        self._sources[source.id] = source
        return source.id

    def get_source(self, source_id: UUID) -> Source | None:
        return self._sources.get(source_id)

    def list_sources(self) -> list[Source]:
        return list(self._sources.values())

    # ---------------------------------------------------------
    # EVIDENCE OPERATIONS
    # ---------------------------------------------------------

    def add_evidence(self, evidence: Evidence) -> UUID:
        if evidence.source_id not in self._sources:
            raise ValueError(
                f"Source {evidence.source_id} does not exist."
            )

        self._evidence[evidence.id] = evidence
        return evidence.id

    def get_evidence(self, evidence_id: UUID) -> Evidence | None:
        return self._evidence.get(evidence_id)

    def list_evidence(self) -> list[Evidence]:
        return list(self._evidence.values())

    def get_evidence_for_source(
        self,
        source_id: UUID,
    ) -> list[Evidence]:
        return [
            evidence
            for evidence in self._evidence.values()
            if evidence.source_id == source_id
        ]

    def count_sources(self) -> int:
        return len(self._sources)

    def count_evidence(self) -> int:
        return len(self._evidence)