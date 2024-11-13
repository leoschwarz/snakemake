from snakemake.common.prefix_lookup import PrefixLookup


def test_basic_match():
    lookup = PrefixLookup([
        ("hello", "world"),
        ("hi", "there")
    ])
    assert lookup.match("hello") == {"world"}
    assert lookup.match("hi") == {"there"}


def test_multiple_matches():
    lookup = PrefixLookup([
        ("a", 1),
        ("ab", 2),
        ("abc", 3)
    ])
    assert lookup.match("abc") == {1, 2, 3}
    assert lookup.match("ab") == {1, 2}
    assert lookup.match("a") == {1}


def test_no_matches():
    lookup = PrefixLookup([
        ("hello", 1),
        ("world", 2)
    ])
    assert lookup.match("xyz") == set()
    assert lookup.match("he") == set()


def test_empty_input():
    lookup = PrefixLookup([
        ("", 1),
        ("a", 2)
    ])
    assert lookup.match("") == {1}
    assert lookup.match("anything") == {1, 2}


def test_empty_lookup():
    lookup = PrefixLookup([])
    assert lookup.match("anything") == set()


def test_overlapping_prefixes():
    lookup = PrefixLookup([
        ("test", 1),
        ("testing", 2),
        ("test", 3),  # Duplicate prefix
    ])
    assert lookup.match("testing") == {1, 2, 3}
    assert lookup.match("test") == {1, 3}


def test_case_sensitivity():
    lookup = PrefixLookup([
        ("Test", 1),
        ("test", 2),
        ("TEST", 3)
    ])
    assert lookup.match("Test") == {1}
    assert lookup.match("test") == {2}
    assert lookup.match("TEST") == {3}


def test_special_characters():
    lookup = PrefixLookup([
        (" ", 1),  # Space
        ("\t", 2),  # Tab
        ("\n", 3),  # Newline
        ("$#@!", 4),  # Special characters
        ("test$", 5)
    ])
    assert lookup.match(" hello") == {1}
    assert lookup.match("\tworld") == {2}
    assert lookup.match("\ntest") == {3}
    assert lookup.match("$#@!test") == {4}
    assert lookup.match("test$abc") == {5}


def test_unicode_characters():
    lookup = PrefixLookup([
        ("é", 1),
        ("ñ", 2),
        ("🌟", 3),
        ("é日本", 4)
    ])
    assert lookup.match("étest") == {1}
    assert lookup.match("ñtest") == {2}
    assert lookup.match("🌟test") == {3}
    assert lookup.match("é日本語") == {1, 4}


def test_sorting_behavior():
    # Test that internal sorting doesn't affect matching
    lookup1 = PrefixLookup([
        ("b", 1),
        ("a", 2),
        ("c", 3)
    ])
    lookup2 = PrefixLookup([
        ("a", 2),
        ("c", 3),
        ("b", 1)
    ])
    assert lookup1.match("b") == lookup2.match("b")
    assert lookup1.match("abc") == lookup2.match("abc")


def test_different_value_types():
    lookup = PrefixLookup([
        ("int", 42),
        ("str", "hello"),
        ("list", (1, 2, 3)),
        ("none", None)
    ])
    assert lookup.match("int_test") == {42}
    assert lookup.match("str_test") == {"hello"}
    assert lookup.match("list_test") == {(1, 2, 3)}
    assert lookup.match("none_test") == {None}


def test_very_long_strings():
    long_prefix = "a" * 1000
    long_key = "a" * 2000
    lookup = PrefixLookup([
        (long_prefix, "value")
    ])
    assert lookup.match(long_key) == {"value"}
    assert lookup.match(long_prefix) == {"value"}
    assert lookup.match("a" * 999) == set()


def test_edge_cases():
    lookup = PrefixLookup([
        ("", "empty"),  # Empty string
        (" ", "space"),  # Single space
        ("  ", "spaces"),  # Multiple spaces
        ("\x00", "null"),  # Null character
    ])
    assert lookup.match("anything") == {"empty"}
    assert lookup.match(" test") == {"empty", "space"}
    assert lookup.match("  test") == {"empty", "space", "spaces"}
    assert lookup.match("\x00test") == {"empty", "null"}
