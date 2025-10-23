from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Consonant:
    """Container for consonant letters."""

    letters: str = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

    def __str__(self) -> str:
        return "Consonant"


@dataclass(frozen=True)
class Vowel:
    """Container for vowel letters."""

    letters: str = "aeiouAEIOU"

    def __str__(self) -> str:
        return "Vowel"
