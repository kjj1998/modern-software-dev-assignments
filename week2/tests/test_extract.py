import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_llm_bullet_list():
    text = """
    - Buy groceries
    - Schedule dentist appointment
    - Fix the leaking faucet
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "groceries" in joined
    assert "dentist" in joined
    assert "faucet" in joined


def test_llm_keyword_prefixed_lines():
    text = """
    todo: Update the README
    action: Review pull request #42
    next: Deploy to staging
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "readme" in joined
    assert "pull request" in joined
    assert "staging" in joined


def test_llm_empty_input():
    items = extract_action_items_llm("")
    assert isinstance(items, list)
    assert len(items) == 0


def test_llm_no_action_items():
    text = "The weather today is sunny and warm. I enjoyed my lunch."
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) == 0


def test_llm_mixed_format():
    text = """
    Meeting notes:
    We discussed the roadmap. Everyone is happy with progress.
    - [ ] Write unit tests for auth module
    * Refactor database layer
    todo: Set up CI pipeline
    Also remember to update the docs.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "test" in joined
    assert "database" in joined or "refactor" in joined
    assert "ci" in joined or "pipeline" in joined
