from .solution import Solution


class Problem:
    """Base problem class"""

    goal: str
    solution: Solution

    def __init__(self):
        self.goal = None
        self.data = None
        self.solution = None

    def set_goal(self, goal: str) -> None:
        self.goal = goal

    def set_data(self, data: dict) -> None:
        self.data = data

    def set_solution(self, solution: Solution) -> None:
        self.solution = solution

    def verify(self) -> bool:
        if self.solution is None:
            return False

        # check solution
        for line in self.data:
            if self.solution.run(line[0]) != line[1]:
                print(f"Failed on input: {line[0]} to produce {line[1]}")
                return False
        return True
