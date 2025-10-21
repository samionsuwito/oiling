class Consonant:
    def __init__(self, letters: str = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"):
        self.letters = letters

    def __str__(self) -> str:
        return "Consonant"


class Vowel:
    def __init__(self, letters: str = "aeiouAEIOU"):
        self.letters = letters

    def __str__(self) -> str:
        return "Vowel"
