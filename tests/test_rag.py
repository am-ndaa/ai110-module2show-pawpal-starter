from pathlib import Path

from rag_utils import build_rag_answer, load_knowledge_base, retrieve_relevant_context


def test_load_knowledge_base_reads_file(tmp_path):
    kb_path = tmp_path / "pet_care_kb.txt"
    kb_path.write_text(
        "Dogs need daily walks and fresh water.\n"
        "Cats enjoy short play sessions and clean litter boxes.\n",
        encoding="utf-8",
    )

    entries = load_knowledge_base(kb_path)

    assert len(entries) == 2
    assert "Dogs" in entries[0]["text"]


def test_retrieve_relevant_context_prefers_keyword_matches(tmp_path):
    kb_path = tmp_path / "pet_care_kb.txt"
    kb_path.write_text(
        "Dogs need daily walks and fresh water.\n"
        "Cats enjoy short play sessions and clean litter boxes.\n"
        "Hamsters need cage cleaning weekly.\n",
        encoding="utf-8",
    )

    entries = load_knowledge_base(kb_path)
    relevant = retrieve_relevant_context("dog exercise schedule", entries)

    assert relevant
    assert "walks" in relevant[0]["text"].lower()


def test_build_rag_answer_uses_context(tmp_path):
    kb_path = tmp_path / "pet_care_kb.txt"
    kb_path.write_text(
        "Dogs need daily walks and fresh water.\n"
        "Cats enjoy short play sessions and clean litter boxes.\n",
        encoding="utf-8",
    )

    entries = load_knowledge_base(kb_path)
    answer = build_rag_answer("How should I care for a dog?", entries)

    assert "dog" in answer.lower()
    assert "walk" in answer.lower() or "daily" in answer.lower()
