from pathlib import Path
import re
from typing import List


def text_to_paragraphs(text: str):

    return [p.strip() for p in text.split("\n\n") if p.strip()]

def score_paragraph(query_tokens, paragraph):

    p = paragraph.lower()
    return sum(1 for token in query_tokens if token in p)

def search_markdown(search_dir: str, query: str) -> List[str]:
    """
    Very simple local markdown search:
    - scans all .md files
    - returns paragraphs containing query keywords
    """

    results: List[str] = []
    path = Path(search_dir)

    if not path.exists():
        return results

    keywords = [w.lower() for w in query.split() if len(w) > 3]

    for md_file in path.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        paragraphs = text.split("\n\n")

        for p in paragraphs:
            content = p.strip()
            if not content:
                continue

            score = sum(k in content.lower() for k in keywords)
            if score >= 1:
                results.append(
                    f"[{md_file.name}]\n{content}"
                )

    return results