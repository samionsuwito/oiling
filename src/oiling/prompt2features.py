from __future__ import annotations

from typing import Dict, Tuple

try:
    from nltk import pos_tag, word_tokenize
    from nltk.stem import WordNetLemmatizer
except Exception:  # pragma: no cover - optional dependency
    pos_tag = None
    word_tokenize = None
    WordNetLemmatizer = None

FeatureBundle = Dict[str, str]


def english_prompt_to_request(text: str) -> Tuple[str, FeatureBundle]:
    """
    Map a simple English prompt to a (lemma, feature bundle) pair.
    """
    s = text.strip().lower()

    if not s:
        return "", {}

    # Use NLTK when available for richer lemmatization.
    nltk_guess = _nltk_guess(s)
    if nltk_guess:
        return nltk_guess

    # gpt heuristics
    # # 'to <verb>' -> bare verb request
    # if s.startswith("to "):
    #     lemma = s[3:].strip()
    #     return lemma, {"cat": "verb"}

    # # English-specific agent suffixes
    # if s.endswith("ers"):
    #     base = s[:-3]
    #     lemma = base[:-2] if base.endswith("er") else base
    #     return lemma, {"cat": "agent", "num": "pl"}

    # if s.endswith("er"):
    #     lemma = s[:-2]
    #     return lemma, {"cat": "agent", "num": "sg"}

    # # Fallback: treat as verb lemma
    # return s, {"cat": "verb"}


def _nltk_guess(text: str) -> Tuple[str, FeatureBundle] | None:
    """Best-effort prompt parsing when NLTK resources are present."""

    if not (word_tokenize and pos_tag and WordNetLemmatizer):
        return None

    try:
        tokens = word_tokenize(text)
        if not tokens:
            return None

        tags = pos_tag(tokens)
        lemma = WordNetLemmatizer().lemmatize(tags[-1][0])
        tag = tags[-1][1]
    except LookupError:
        print("NLTK not available")
        # Required models not downloaded; caller falls back to heuristics.
        return None

    if tag.startswith("VB"):
        return lemma, {"cat": "verb"}

    if tag in ("NN", "NNS") and lemma.endswith("er"):
        number = "pl" if tag == "NNS" else "sg"
        return lemma[:-2], {"cat": "agent", "num": number}

    return None
