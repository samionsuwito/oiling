from .morph_engine import CircumfixRule, FeatureBundle, Generator, Lexeme, MorphRule, PrefixRule, RewriteRule, SuffixRule, TemplateRule
from .morphology import MorphologyProblem, MorphologySolution
from .problem import Problem
from .prompt2features import english_prompt_to_request
from .solution import Rule, Solution

__all__ = [
    "Problem",
    "Solution",
    "Rule",
    "MorphologyProblem",
    "Generator",
    "Lexeme",
    "FeatureBundle",
    "MorphRule",
    "MorphologySolution",
    "PrefixRule",
    "SuffixRule",
    "CircumfixRule",
    "TemplateRule",
    "RewriteRule",
    "english_prompt_to_request",
]
# import nltk
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('punkt_tab')
