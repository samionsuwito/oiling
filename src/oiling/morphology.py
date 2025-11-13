from __future__ import annotations

import json
from typing import Dict, Iterable, Mapping, List, Tuple, Literal, Set

from .morph_engine import Generator, Lexeme, MorphRule, FeatureBundle
from .problem import Problem
from .prompt2features import english_prompt_to_request
from .solution import Solution
from .utils import ParadigmTableFormatter

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

    def infer_paradigm(self) -> List[Tuple[str, FeatureBundle]]:
        """
        Automatically infer paradigm feature combinations from the rules.

        Analyzes all rules to determine what feature combinations are possible,
        then generates labeled column definitions.

        Returns:
            List of (label, features) tuples for paradigm columns
        """
        if not self._generator.rules:
            return []

        # Collect all unique feature bundles from rules
        paradigm: List[Tuple[str, FeatureBundle]] = []
        seen_bundles: Set[str] = set()

        # Start with empty/base form
        paradigm.append(("base", {}))
        seen_bundles.add(json.dumps({}, sort_keys=True))

        # Add each rule's feature requirement as a column
        for rule in sorted(self._generator.rules, key=lambda r: r.order):
            bundle_key = json.dumps(rule.when, sort_keys=True)
            if bundle_key not in seen_bundles:
                seen_bundles.add(bundle_key)
                label = self._create_label(rule.when)
                paradigm.append((label, dict(rule.when)))

        return paradigm

    def _create_label(self, features: FeatureBundle) -> str:
        """Create a readable label from feature bundle"""
        if not features:
            return "base"

        # Common feature abbreviations
        abbrev = {
            "num": {"sg": "SG", "pl": "PL"},
            "tense": {"past": "PST", "pres": "PRS", "fut": "FUT"},
            "person": {"1": "1", "2": "2", "3": "3"},
            "cat": {"verb": "V", "noun": "N", "adj": "ADJ", "agent": "AGT"},
            "polarity": {"neg": "NEG", "pos": "POS"},
            "class": lambda x: f"CL{x}",
        }

        parts = []
        for key in sorted(features.keys()):
            value = features[key]
            if key in abbrev:
                if callable(abbrev[key]):
                    parts.append(abbrev[key](value))
                elif value in abbrev[key]:
                    parts.append(abbrev[key][value])
                else:
                    parts.append(f"{key}={value}")
            else:
                parts.append(f"{key}={value}")

        return ".".join(parts)

    def get_auto_table(
        self,
        lexeme_subset: List[str] | None = None,
        format: Literal["pretty", "json"] = "pretty",
    ) -> str:
        """
        Generate paradigm table with automatically inferred feature combinations.

        Args:
            lexeme_subset: Optional list of lemma names to include. If None, includes all lexemes.
            format: Output format - "pretty" for human-readable Unicode table,
                   "json" for LLM-readable structured data.

        Returns:
            Formatted table string (pretty) or JSON string (json)
        """
        paradigm = self.infer_paradigm()
        return self.get_table(paradigm, lexeme_subset, format)

    def get_table(
        self,
        feature_combinations: List[Tuple[str, FeatureBundle]],
        lexeme_subset: List[str] | None = None,
        format: Literal["pretty", "json"] = "pretty",
    ) -> str:
        """
        Generate a paradigm table with rules as column headers and lexemes as rows.

        Args:
            feature_combinations: List of (label, features) tuples for each column.
                                 Example: [("singular", {"num": "sg"}), ("plural", {"num": "pl"})]
            lexeme_subset: Optional list of lemma names to include. If None, includes all lexemes.
            format: Output format - "pretty" for human-readable Unicode table,
                   "json" for LLM-readable structured data.

        Returns:
            Formatted table string (pretty) or JSON string (json)
        """
        formatter = ParadigmTableFormatter(self._generator, self._lexicon)
        return formatter.format_table(feature_combinations, lexeme_subset, format)
