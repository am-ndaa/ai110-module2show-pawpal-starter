from pathlib import Path
from typing import List, Dict


def load_knowledge_base(path: str | Path | None = None) -> List[Dict[str, str]]:
    """Load a simple local knowledge base from a text file."""
    kb_path = Path(path or Path(__file__).with_name("pet_care_kb.txt"))
    if not kb_path.exists():
        return []

    entries = []
    for line in kb_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append({"text": line})
    return entries


def retrieve_relevant_context(query: str, entries: List[Dict[str, str]], limit: int = 3) -> List[Dict[str, str]]:
    """Return the most relevant knowledge-base entries for a query."""
    query_lower = query.lower()
    scored = []
    for entry in entries:
        text = entry["text"].lower()
        score = sum(word in text for word in query_lower.split())
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [entry for _, entry in scored[:limit]]


def build_rag_answer(query: str, entries: List[Dict[str, str]]) -> str:
    """Build a simple answer from relevant context entries."""
    relevant = retrieve_relevant_context(query, entries)
    if not relevant:
        return "I don’t have enough pet-care guidance for that question yet."

    context_text = "\n".join(entry["text"] for entry in relevant)
    return f"Based on the knowledge base:\n{context_text}\n\nAnswer: {query}"
