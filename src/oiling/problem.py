from __future__ import annotations

from typing import Optional, Sequence, Tuple

from .solution import Solution

Example = Tuple[str, str]


class Problem:
    """Base problem definition containing goal, data, and solution."""

    goal: Optional[str]
    data: Optional[Sequence[Example]]
    solution: Optional[Solution]

    def __init__(self) -> None:
        self.goal = None
        self.data = None
        self.solution = None

    def set_goal(self, goal: str) -> None:
        self.goal = goal

    def set_data(self, data: Sequence[Example]) -> None:
        self.data = data

    def set_solution(self, solution: Solution) -> None:
        self.solution = solution

    def verify(self) -> bool:
        if self.solution is None or self.data is None:
            return False

        for idx, (source, expected) in enumerate(self.data, start=1):
            actual = self.solution.run(source)
            if actual != expected:
                print(
                    f"Example {idx} failed: prompt '{source}' expected '{expected}' but produced '{actual}'"
                )
                return False
        return True
