class Rule:
    """Solution rule"""

    def __init__(self):
        self.description = ""

    def apply(self, data: str) -> str:
        return data


class Solution:
    """A solution is a set of rules"""

    def __init__(self):
        self.rules = []

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def get_rules(self) -> list:
        return self.rules

    def pretty_print(self) -> None:
        for idx, rule in enumerate(self.rules, start=1):
            print(f"Rule {idx}: {rule.description}")

    def run(self, data: str) -> str:
        result = data
        # change later to actual processing
        for rule in self.rules:
            result = rule.apply(result)
        return result
