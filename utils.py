"""노트 파일을 읽고 파싱하는 유틸리티.

notes/ 폴더 안의 마크다운 파일을 스캔한다.
파일명 규칙:  YYYY-MM-DD_주제.md   (예: 2026-07-26_선형대수-벡터.md)
파일 맨 위에 선택적으로 YAML 프론트매터를 넣을 수 있다:

---
stage: 선형대수
tags: [벡터, 내적]
---
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

NOTES_DIR = Path(__file__).parent / "notes"
FNAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[_-](.+)\.md$")


@dataclass
class Note:
    path: Path
    day: date
    title: str
    body: str
    stage: str = "기타"
    tags: list[str] = field(default_factory=list)

    @property
    def word_count(self) -> int:
        return len(self.body.split())


def _parse_front_matter(text: str) -> tuple[dict, str]:
    """아주 단순한 프론트매터 파서 (PyYAML 의존 없음)."""
    meta: dict = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            raw = text[3:end].strip()
            body = text[end + 3 :].lstrip("\n")
            for line in raw.splitlines():
                if ":" not in line:
                    continue
                key, val = line.split(":", 1)
                key, val = key.strip(), val.strip()
                if val.startswith("[") and val.endswith("]"):
                    meta[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
                else:
                    meta[key] = val
            return meta, body
    return meta, text


def load_notes() -> list[Note]:
    """notes/ 폴더의 모든 노트를 최신순으로 반환."""
    notes: list[Note] = []
    if not NOTES_DIR.exists():
        return notes

    for p in NOTES_DIR.rglob("*.md"):  # 하위 폴더까지 재귀 스캔
        m = FNAME_RE.match(p.name)
        raw = p.read_text(encoding="utf-8")
        meta, body = _parse_front_matter(raw)

        if m:
            day = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            title = m.group(2).replace("-", " ").replace("_", " ").strip()
        else:
            day = datetime.fromtimestamp(p.stat().st_mtime).date()
            title = p.stem

        # 단계(카테고리) = 상위 폴더명. 루트에 바로 있으면 프론트매터 or "기타".
        if p.parent != NOTES_DIR:
            stage = p.parent.name
        else:
            stage = meta.get("stage", "기타")

        notes.append(
            Note(
                path=p,
                day=day,
                title=meta.get("title", title),
                body=body,
                stage=stage,
                tags=meta.get("tags", []),
            )
        )

    notes.sort(key=lambda n: n.day, reverse=True)
    return notes


def study_streak(notes: list[Note]) -> int:
    """오늘 또는 어제부터 연속으로 노트를 남긴 일수."""
    if not notes:
        return 0
    days = sorted({n.day for n in notes}, reverse=True)
    today = date.today()
    if (today - days[0]).days > 1:
        return 0
    streak = 1
    for prev, cur in zip(days, days[1:]):
        if (prev - cur).days == 1:
            streak += 1
        else:
            break
    return streak
