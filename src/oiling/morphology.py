from .problem import Problem
from .solution import Rule
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


class MorphologyProblem(Problem):
    """Morphology problem class"""

    def __init__(self):
        super().__init__()
        self.rosetta = True


class POSRule(Rule):
    """POS rule for morphology"""

    def __init__(self, description: str):
        self.description = description
        self.condition = None
        self.translation = {}
        self.word = True  # whether this rule applies to only words

    def set_condition(self, condition: str) -> None:
        self.condition = condition

    def check_condition(self, data: str) -> bool:
        # check https://hannibunny.github.io/nlpbook/03postagging/02PosTagging.html for custom conditions
        if not self.condition:
            raise ValueError("Condition not set for TypeRule")
        # check https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for POS tags
        if pos_tag(word_tokenize(data))[-1][1] == self.condition:
            return True
        return False

    def set_translation(self, translation: tuple[str, str]) -> None:
        self.translation[translation[0]] = translation[1]

    def get_translation(self, phrase: str) -> str:
        return self.translation.get(phrase, phrase)

    def apply(self, data: str) -> str:
        if not self.condition:
            raise ValueError("Condition not set for TypeRule")
        if self.word:
            if self.check_condition(data):
                return self.get_translation(data)
        return data
