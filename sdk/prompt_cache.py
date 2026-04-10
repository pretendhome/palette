"""Prompt cache preservation helpers.

The goal is simple: keep stable prompt prefix text byte-for-byte identical
across turns, and isolate volatile task/session data at the end.

This does not implement model-specific caching. It gives Palette agents a
deterministic way to construct cache-friendly prompt bundles that callers can
map onto their provider of choice.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable


def _normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def _coerce_json(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return _normalize_text(value)
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PromptSection:
    """A named chunk of prompt text."""

    name: str
    content: str
    cacheable: bool = True

    def normalized_content(self) -> str:
        return _normalize_text(self.content)

    def render(self) -> str:
        body = self.normalized_content()
        if not body:
            return ""
        return f"## {self.name}\n{body}"


@dataclass(frozen=True)
class PromptBundle:
    """A cache-friendly prompt split into stable prefix and volatile suffix."""

    stable_sections: tuple[PromptSection, ...]
    volatile_sections: tuple[PromptSection, ...]

    @property
    def stable_prefix(self) -> str:
        return "\n\n".join(
            part for part in (section.render() for section in self.stable_sections) if part
        )

    @property
    def volatile_suffix(self) -> str:
        return "\n\n".join(
            part for part in (section.render() for section in self.volatile_sections) if part
        )

    @property
    def full_prompt(self) -> str:
        parts = [self.stable_prefix, self.volatile_suffix]
        return "\n\n".join(part for part in parts if part)

    @property
    def stable_hash(self) -> str:
        return _sha256(self.stable_prefix)

    @property
    def full_hash(self) -> str:
        return _sha256(self.full_prompt)

    def cache_metadata(self) -> dict[str, object]:
        return {
            "stable_hash": self.stable_hash,
            "full_hash": self.full_hash,
            "stable_sections": [section.name for section in self.stable_sections],
            "volatile_sections": [section.name for section in self.volatile_sections],
        }


def build_prompt_bundle(
    stable_sections: Iterable[PromptSection],
    volatile_sections: Iterable[PromptSection],
) -> PromptBundle:
    """Build a prompt bundle while preserving stable/volatile ordering."""

    return PromptBundle(
        stable_sections=tuple(section for section in stable_sections if section.normalized_content()),
        volatile_sections=tuple(section for section in volatile_sections if section.normalized_content()),
    )


def packet_payload_to_section(name: str, value: object, *, cacheable: bool = False) -> PromptSection:
    """Convenience helper for packet/task data that should usually stay volatile."""

    return PromptSection(name=name, content=_coerce_json(value), cacheable=cacheable)
