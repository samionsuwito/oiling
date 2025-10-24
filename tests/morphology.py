import oiling as oil


def test_generalized_morphology():
    rules = [
        oil.CircumfixRule(
            name="agent-sg",
            when={"cat": "agent", "num": "sg"},
            pre="um",
            post="i",
            order=10,
        ),
        oil.CircumfixRule(
            name="agent-pl",
            when={"cat": "agent", "num": "pl"},
            pre="aba",
            post="i",
            order=10,
        ),
        oil.SuffixRule(
            name="verb-bare",
            when={"cat": "verb"},
            suffix="a",
            order=20,
        ),
    ]
    lexicon = {
        "paint": oil.Lexeme.create("paint", "dweb"),
        "hunt": oil.Lexeme.create("hunt", "zingel"),
        "kill": oil.Lexeme.create("kill", "bulal"),
        "carve": oil.Lexeme.create("carve", "baz"),
    }

    solution = oil.MorphologySolution(rules, lexicon)

    problem = oil.MorphologyProblem()
    data = [
        ("to paint", "dweba"),
        ("hunter", "umzingeli"),
        ("killers", "ababulali"),
        ("to kill", "bulala"),
        ("carver", "umbazi"),
        ("to carve", "baza"),
    ]
    problem.set_data(data)

    problem.set_solution(solution)
    assert problem.verify()


if __name__ == "__main__":
    test_generalized_morphology()
