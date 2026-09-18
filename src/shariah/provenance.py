"""Source register loading and provenance records."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SOURCE_REGISTER_PATH = ROOT / "docs" / "shariah" / "source_register.json"


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    authority: str
    organization: str
    document_title: str
    standard_number: str
    publication_date: str
    version: str
    section: str
    clause: str
    page: str
    url: str
    access_date: str
    authority_level: str
    scope: str
    notes: str
    verification_status: str
    sha256: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def load_source_register(path: Path | None = None) -> list[SourceRecord]:
    payload = json.loads((path or SOURCE_REGISTER_PATH).read_text(encoding="utf-8"))
    rows = payload["sources"] if isinstance(payload, dict) else payload
    return [SourceRecord(**{k: row.get(k) for k in SourceRecord.__dataclass_fields__}) for row in rows]


def source_by_id(source_id: str, register: list[SourceRecord] | None = None) -> SourceRecord:
    items = register if register is not None else load_source_register()
    for row in items:
        if row.source_id == source_id:
            return row
    raise KeyError(source_id)
