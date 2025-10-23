from __future__ import annotations

from typing import Dict, Iterable

from .morph_engine import Generator, Lexeme
from .prompt2features import english_prompt_to_request
from .solution import Rule


class RootedMorphRule(Rule):
    """
    The rule interprets an English prompt, looks up the lexeme, then delegates
    to Generator to realize the target surface form. Unknown prompts fall
    through unchanged to allow chaining with other rules.
    """

    def __init__(
        self, description: str, generator: Generator, lexicon: Dict[str, Lexeme]
    ):
        super().__init__()
        self.description = description
        self._generator = generator
        self._lexicon = lexicon

    def apply(self, data: str) -> str:
        lemma, feats = english_prompt_to_request(data)
        if not lemma:
            return data

        lexeme = self._resolve_lexeme(lemma)
        if lexeme is None:
            return data

        return self._generator.generate(lexeme, feats)

    def _resolve_lexeme(self, lemma: str) -> Lexeme | None:
        for candidate in self._lemma_candidates(lemma):
            lexeme = self._lexicon.get(candidate)
            if lexeme is not None:
                return lexeme
        return None

    def _lemma_candidates(self, lemma: str) -> Iterable[str]:
        seen = set()
        for candidate in (lemma, *self._lemma_variants(lemma)):
            if candidate not in seen:
                seen.add(candidate)
                yield candidate

    def _lemma_variants(self, lemma: str) -> Iterable[str]:
        if lemma and lemma[-1] not in "aeiou":
            yield f"{lemma}e"
        if len(lemma) > 1 and lemma[-1] == lemma[-2]:
            yield lemma[:-1]
