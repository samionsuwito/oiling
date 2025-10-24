from __future__ import annotations

from typing import Dict, Iterable, Mapping, List

from .morph_engine import Generator, Lexeme, MorphRule
from .problem import Problem
from .prompt2features import english_prompt_to_request
from .solution import Solution

try:
    from nltk.tag import pos_tag  # type: ignore
    from nltk.tokenize import word_tokenize  # type: ignore
except Exception:  # pragma: no cover - keep optional dependency
    pos_tag = None
    word_tokenize = None


class MorphologyProblem(Problem):
    """Morphology problem class"""

    def __init__(self):
        super().__init__()
        self.rosetta = True


class MorphologySolution(Solution):
    """
    Specialized solution that wires prompt parsing, lexeme lookup, and the morphology generator.
    """

    def __init__(
        self,
        rules: Iterable[MorphRule],
        lexicon: Mapping[str, Lexeme],
        description: str = "Morphology solution",
    ) -> None:
        super().__init__()
        self.description = description
        self._generator = Generator(rules)
        self._lexicon = dict(lexicon)

    @property
    def generator(self) -> Generator:
        return self._generator

    @property
    def morph_rules(self) -> List[MorphRule]:
        return list(self._generator.rules)

    @property
    def lexicon(self) -> Dict[str, Lexeme]:
        return dict(self._lexicon)

    def run(self, data: str) -> str:
        lemma, feats = english_prompt_to_request(data)
        result = data
        if lemma:
            lexeme = self._resolve_lexeme(lemma)
            if lexeme is not None:
                result = self._generator.generate(lexeme, feats)

        return super().run(result)

    def _resolve_lexeme(self, lemma: str) -> Lexeme | None:
        for candidate in self._lemma_candidates(lemma):
            if candidate in self._lexicon:
                return self._lexicon[candidate]
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
