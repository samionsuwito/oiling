class Consonant:
    def __init__(self):
        self.letters = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    
    def __init__(self, letters: str):
        self.letters = letters

    def __str__(self) -> str:
        return "Consonant"

class Vowel:
    def __init__(self):
        self.letters = "aeiouAEIOU"
    
    def __init__(self, letters: str):
        self.letters = letters

    def __str__(self) -> str:
        return "Vowel"