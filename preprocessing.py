"""
preprocessing.py
-----------------
Basic NLP text preprocessing utilities used before feeding text into the
TF-IDF vectorizer: lowercasing, punctuation removal, and whitespace
normalization.
"""

import re


def clean_text(text: str) -> str:
    """Lowercases, strips punctuation, and normalizes whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
