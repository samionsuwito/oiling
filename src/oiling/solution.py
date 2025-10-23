from __future__ import annotations

from typing import Iterable, List


class Rule:
    """Base class for solution rules."""

    description: str

    def __init__(self, description: str = "") -> None:
        self.description = description

    def apply(self, data: str) -> str:
        """Return the transformed data. Override in subclasses."""

        return data


class Solution:
    """A solution is an ordered collection of rules."""

    def __init__(self) -> None:
        self._rules: List[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def get_rules(self) -> List[Rule]:
        return list(self._rules)

    def pretty_print(self) -> None:
        for idx, rule in enumerate(self._rules, start=1):
            print(f"Rule {idx}: {rule.description}")

    def run(self, data: str) -> str:
        result = data
        for rule in self._rules:
            result = rule.apply(result)
        return result

    def __iter__(self) -> Iterable[Rule]:
        return iter(self._rules)
