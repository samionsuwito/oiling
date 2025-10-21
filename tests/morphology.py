import oiling as oil


# From Linguistics Olympiad Training Guide Problem 5.1
def simple_test():
    problem = oil.MorphologyProblem()
    problem.set_goal(
        "Translate into Zulu 'to paint', 'hunter', 'killers', 'to kill', 'carver', 'to carve'"
    )
    data = [
        ("painter", "umdwebi"),
        ("hunters", "abazingeli"),
        ("killer" , "umbulali"),
        ("painters", "abadwebi"),
        ("to hunt", "zingela"),
        ("carvers", "ababazi"),
    ]
    problem.set_data(data)
    solution = oil.Solution()

    rule1 = oil.POSRule("Singular Noun")
    rule1.set_condition("NN")
    rule1.set_translation(data[0])
    rule1.set_translation(data[2])
    solution.add_rule(rule1)

    rule2 = oil.POSRule("Plural Noun")
    rule2.set_condition("NNS")
    rule2.set_translation(data[1])
    rule2.set_translation(data[3])
    rule2.set_translation(data[5])
    solution.add_rule(rule2)

    rule3 = oil.POSRule("Verb")
    rule3.set_condition("VB")
    rule3.set_translation(data[4])
    solution.add_rule(rule3)

    problem.set_solution(solution)
    assert problem.verify()


if __name__ == "__main__":
    simple_test()
