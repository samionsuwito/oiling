from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Protocol


FeatureBundle = Dict[str, Any]


@dataclass(frozen=True)
class Lexeme:
    """Language-agnostic lexeme entry with optional irregular overrides."""

    lemma: str
    stem: str
    features: FeatureBundle = field(default_factory=dict)
    irregular: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        lemma: str,
        stem: str,
        *,
        features: FeatureBundle | None = None,
        irregular: Dict[str, str] | None = None,
    ) -> Lexeme:
        """
        Convenience constructor that mirrors the dataclass signature while making intent explicit.
        """

        return cls(
            lemma=lemma,
            stem=stem,
            features=features or {},
            irregular=irregular or {},
        )


class Applies(Protocol):
    """Callable protocol for feature preconditions."""

    def __call__(self, feats: FeatureBundle) -> bool: ...


def _match(feats: FeatureBundle, need: FeatureBundle) -> bool:
    """Return True when all items in need match feats."""

    for key, value in need.items():
        if feats.get(key) != value:
            return False
    return True


@dataclass
class MorphRule:
    """Base class for feature-conditional surface edits."""

    name: str
    when: FeatureBundle
    order: int = 0

    def applies(self, feats: FeatureBundle) -> bool:
        return _match(feats, self.when)

    def apply(
        self, surface: str, feats: FeatureBundle
    ) -> str:  # pragma: no cover - override
        return surface


@dataclass
class PrefixRule(MorphRule):
    """Add a prefix when preconditions are met."""

    prefix: str = ""

    def apply(self, surface: str, feats: FeatureBundle) -> str:
        return self.prefix + surface if self.applies(feats) else surface


@dataclass
class SuffixRule(MorphRule):
    """Add a suffix when preconditions are met."""

    suffix: str = ""

    def apply(self, surface: str, feats: FeatureBundle) -> str:
        return surface + self.suffix if self.applies(feats) else surface


@dataclass
class CircumfixRule(MorphRule):
    """Add both prefix and suffix when preconditions are met."""

    pre: str = ""
    post: str = ""

    def apply(self, surface: str, feats: FeatureBundle) -> str:
        return self.pre + surface + self.post if self.applies(feats) else surface


@dataclass
class TemplateRule(MorphRule):
    """Apply a templatic pattern that interpolates the stem into a template."""

    template: str = ""

    def apply(self, surface: str, feats: FeatureBundle) -> str:
        return (
            self.template.replace("{STEM}", surface) if self.applies(feats) else surface
        )


@dataclass
class RewriteRule(MorphRule):
    """Apply a regex rewrite after morphological composition."""

    pattern: str = ""
    repl: str = ""
    flags: int = 0

    def apply(self, surface: str, feats: FeatureBundle) -> str:
        if not self.applies(feats) or not self.pattern:
            return surface
        return re.sub(self.pattern, self.repl, surface, flags=self.flags)


class Generator:
    """Compose rules to derive a surface realization for a lexeme."""

    def __init__(self, rules: Iterable[MorphRule]):
        self.rules: List[MorphRule] = sorted(list(rules), key=lambda rule: rule.order)

    def generate(self, lexeme: Lexeme, target: FeatureBundle) -> str:
        """Return the surface form for the given target feature bundle."""

        signature = self._signature(target)
        if signature in lexeme.irregular:
            return lexeme.irregular[signature]

        surface = lexeme.stem
        feats: FeatureBundle = {**lexeme.features, **target}

        for rule in self.rules:
            if rule.applies(feats):
                surface = rule.apply(surface, feats)

        return surface

    def _signature(self, feats: FeatureBundle) -> str:
        """Stable signature used to look up irregular forms."""

        keys = sorted(feats.keys())
        return "|".join(f"{key}={feats[key]}" for key in keys)
