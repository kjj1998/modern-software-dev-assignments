from __future__ import annotations

import re
from typing import List
from ollama import chat
from pydantic import BaseModel

_BULLET_RE = re.compile(r"^\s*([-*•]|\d+\.)\s+")
_CHECKBOX_RE = re.compile(r"^\[(?:\s|todo)\]\s*", re.IGNORECASE)
_KEYWORD_PREFIXES = ("todo:", "action:", "next:")
_IMPERATIVE_VERBS = frozenset({
    "add", "create", "implement", "fix", "update", "write",
    "check", "verify", "refactor", "document", "design", "investigate",
})


def _is_action_line(line: str) -> bool:
    lowered = line.strip().lower()
    if not lowered:
        return False
    return (
        bool(_BULLET_RE.match(lowered))
        or any(lowered.startswith(p) for p in _KEYWORD_PREFIXES)
        or "[ ]" in lowered
        or "[todo]" in lowered
    )


def _clean_line(line: str) -> str:
    cleaned = _BULLET_RE.sub("", line).strip()
    cleaned = _CHECKBOX_RE.sub("", cleaned).strip()
    return cleaned


def _deduplicate(items: List[str]) -> List[str]:
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    return bool(words) and words[0].lower() in _IMPERATIVE_VERBS


def extract_action_items(text: str) -> List[str]:
    extracted = [
        _clean_line(line)
        for line in text.splitlines()
        if line.strip() and _is_action_line(line)
    ]
    if not extracted:
        extracted = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", text.strip())
            if s.strip() and _looks_imperative(s.strip())
        ]
    return _deduplicate(extracted)


class _ActionItemsSchema(BaseModel):
    action_items: List[str]


def extract_action_items_llm(text: str) -> List[str]:
    response = chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": "Extract all action items from the given text. Action items are tasks, to-dos, or things that need to be done.",
            },
            {"role": "user", "content": text},
        ],
        format=_ActionItemsSchema.model_json_schema(),
    )
    result = _ActionItemsSchema.model_validate_json(response.message.content or "")
    return result.action_items
