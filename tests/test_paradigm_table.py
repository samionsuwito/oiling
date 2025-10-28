"""
Test for paradigm table generation.
"""

import json
import oiling as oil


def setup_solution():
    """Create a standard solution for testing"""
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
    }

    return oil.MorphologySolution(rules, lexicon)


def get_paradigm():
    """Get standard paradigm for testing"""
    return [
        ("infinitive", {"cat": "verb"}),
        ("agent.sg", {"cat": "agent", "num": "sg"}),
        ("agent.pl", {"cat": "agent", "num": "pl"}),
    ]


def test_full_paradigm_table():
    """Test generating full paradigm table"""
    print("Test: Full paradigm table...")

    solution = setup_solution()
    paradigm = get_paradigm()
    table = solution.get_table(paradigm)

    # Verify table contains expected elements
    assert "┌" in table, "Table should have box-drawing characters"
    assert "Lemma" in table, "Table should have 'Lemma' header"
    assert "infinitive" in table, "Table should have 'infinitive' column"
    assert "agent.sg" in table, "Table should have 'agent.sg' column"
    assert "paint" in table, "Table should have 'paint' row"
    assert "hunt" in table, "Table should have 'hunt' row"
    assert "dweba" in table, "Table should contain 'dweba'"
    assert "umzingeli" in table, "Table should contain 'umzingeli'"
    assert "abazingeli" in table, "Table should contain 'abazingeli'"

    print("✓ Full paradigm table works")


def test_subset_paradigm_table():
    """Test generating paradigm table with subset of lexemes"""
    print("Test: Subset paradigm table...")

    solution = setup_solution()
    paradigm = get_paradigm()
    table_subset = solution.get_table(paradigm, lexeme_subset=["paint"])

    assert "paint" in table_subset, "Subset should contain 'paint'"
    assert "hunt" not in table_subset, "Subset should not contain 'hunt'"

    print("✓ Subset paradigm table works")


def test_edge_cases():
    """Test edge cases like empty paradigm"""
    print("Test: Edge cases...")

    solution = setup_solution()
    empty_table = solution.get_table([])
    assert empty_table == "", "Empty paradigm should return empty string"

    print("✓ Edge cases handled correctly")


def test_backward_compatibility():
    """Test that original functionality still works"""
    print("Test: Backward compatibility...")

    solution = setup_solution()
    problem = oil.MorphologyProblem()
    problem.set_data(
        [
            ("to paint", "dweba"),
            ("hunter", "umzingeli"),
        ]
    )
    problem.set_solution(solution)
    assert problem.verify(), "Problem verification should still work"

    print("✓ Backward compatibility maintained")


def test_json_format():
    """Test JSON format output"""
    print("Test: JSON format...")

    solution = setup_solution()
    paradigm = get_paradigm()
    json_output = solution.get_table(paradigm, format="json")

    # Verify it's valid JSON
    data = json.loads(json_output)
    assert "columns" in data, "JSON should have 'columns' key"
    assert "rows" in data, "JSON should have 'rows' key"
    assert "total_rows" in data, "JSON should have 'total_rows' key"
    assert data["total_rows"] == 2, "Should have 2 rows"
    assert len(data["columns"]) == 4, "Should have 4 columns"
    assert len(data["rows"]) == 2, "Should have 2 data rows"

    # Verify column structure
    for col in data["columns"]:
        assert "name" in col, "Column should have 'name'"
        assert "type" in col, "Column should have 'type'"
        assert col["type"] == "string", "All columns should be string type"

    # Verify data
    assert data["rows"][0][0] == "paint", "First row should be paint"
    assert data["rows"][1][0] == "hunt", "Second row should be hunt"
    assert "dweba" in data["rows"][0], "Should contain dweba"
    assert "umzingeli" in data["rows"][1], "Should contain umzingeli"

    print("✓ JSON format works correctly")


def test_json_format_with_subset():
    """Test JSON format with subset of lexemes"""
    print("Test: JSON format with subset...")

    solution = setup_solution()
    paradigm = get_paradigm()
    json_subset = solution.get_table(paradigm, lexeme_subset=["paint"], format="json")
    data_subset = json.loads(json_subset)
    assert data_subset["total_rows"] == 1, "Subset should have 1 row"
    assert data_subset["rows"][0][0] == "paint", "Should only have paint"

    print("✓ JSON format with subset works")


def test_auto_paradigm_inference():
    """Test automatic paradigm inference"""
    print("Test: Auto paradigm inference...")

    solution = setup_solution()
    inferred = solution.infer_paradigm()
    assert len(inferred) > 0, "Should infer at least base form"
    assert inferred[0] == ("base", {}), "First should be base form"

    # Check that actual rule features are present
    feature_bundles = [feats for _, feats in inferred]
    assert {} in feature_bundles, "Should have empty base form"

    print("✓ Paradigm inference works")


def test_auto_table_generation():
    """Test automatic table generation"""
    print("Test: Auto table generation...")

    solution = setup_solution()
    auto_table = solution.get_auto_table()
    assert "┌" in auto_table, "Auto table should have box-drawing"
    assert "base" in auto_table, "Auto table should have base column"
    assert "paint" in auto_table, "Auto table should have lexemes"

    # Test with JSON format
    auto_json = solution.get_auto_table(format="json")
    auto_data = json.loads(auto_json)
    assert "columns" in auto_data, "Auto JSON should have columns"
    assert "rows" in auto_data, "Auto JSON should have rows"

    print("✓ Auto table generation works")


def test_auto_table_with_subset():
    """Test automatic table generation with subset"""
    print("Test: Auto table with subset...")

    solution = setup_solution()
    auto_subset = solution.get_auto_table(lexeme_subset=["paint"])
    assert "paint" in auto_subset, "Subset should contain paint"
    assert "hunt" not in auto_subset, "Subset should not contain hunt"

    print("✓ Auto table with subset works")


def run_all_tests():
    """Run all tests"""
    tests = [
        test_full_paradigm_table,
        test_subset_paradigm_table,
        test_edge_cases,
        test_backward_compatibility,
        test_json_format,
        test_json_format_with_subset,
        test_auto_paradigm_inference,
        test_auto_table_generation,
        test_auto_table_with_subset,
    ]

    print("=" * 60)
    print("Running Paradigm Table Tests")
    print("=" * 60)
    print()

    for test in tests:
        test()
        print()

    print("=" * 60)
    print("✅ ALL PARADIGM TABLE TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
