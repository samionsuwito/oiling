from .problem import Problem

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
