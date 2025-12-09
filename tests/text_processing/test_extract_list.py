from listy.text_processing import (
    AmbiguousLists,
    ExtractedList,
    NoListFound,
    TooFewItems,
    TooManyItems,
    extract_list,
)


def test_numbered_list_extraction():
    text = """
Some intro text here.

1. First item
2. Second item
3. Third item

Some outro text.
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert result.items == ("First item", "Second item", "Third item")


def test_bullet_list_extraction():
    text = """
Here are some points:

* First bullet
* Second bullet
* Third bullet
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert result.items == ("First bullet", "Second bullet", "Third bullet")


def test_dash_bullet_list():
    text = """
- Item one
- Item two
- Item three
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert result.items == ("Item one", "Item two", "Item three")


def test_picks_longer_list():
    text = """
Short list:
* A
* B

Long list:
1. One
2. Two
3. Three
4. Four
5. Five
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert len(result.items) == 5
    assert result.items[0] == "One"


def test_ambiguous_lists_returns_failure():
    text = """
First list:
1. Alpha
2. Beta
3. Gamma

Second list:
* One
* Two
* Three
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, AmbiguousLists)
    assert len(result.candidates) == 2
    assert ("Alpha", "Beta", "Gamma") in result.candidates
    assert ("One", "Two", "Three") in result.candidates


def test_ambiguity_threshold_zero_picks_longest():
    text = """
First list:
1. Alpha
2. Beta
3. Gamma

Second list:
* One
* Two
* Three
"""
    result = extract_list(text, min_items=0, max_items=None, ambiguity_threshold=0)
    assert isinstance(result, ExtractedList)
    assert len(result.items) == 3


def test_no_list_returns_failure():
    text = "Just some regular text without any list."
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, NoListFound)


def test_min_items_constraint():
    text = """
1. First
2. Second
3. Third
"""
    result = extract_list(text, min_items=5, max_items=None)
    assert isinstance(result, TooFewItems)
    assert result.actual_count == 3


def test_max_items_constraint():
    text = """
1. First
2. Second
3. Third
4. Fourth
5. Fifth
"""
    result = extract_list(text, min_items=0, max_items=3)
    assert isinstance(result, TooManyItems)
    assert result.actual_count == 5


def test_real_world_polish_text():
    text = """
Oto lista wątków poruszanych w przetranskrybowanej treści wiadomości głosowej:

1. Opis domu i stylu życia w Dolinie Krzemowej, w tym nazwy domów i zwyczaj zapraszania się nawzajem.

2. Fałszywa produktywność i spotkania w Dolinie Krzemowej, w tym jeżdżenie taksówkami i korzystanie z usług Waymo.

3. Pojęcie "zakład" i jego znaczenie w Dolinie Krzemowej, w tym przykład laboratoriów badawczych zajmujących się sztuczną inteligencją.

4. Praca w Dolinie Krzemowej, w tym non-stop praca i poświęcanie czasu na programowanie i sprzedaż oprogramowania.

5. Billboardy w San Francisco, w tym te skierowane do twórców oprogramowania.

6. Zwrot "pivot" i jego znaczenie w Dolinie Krzemowej, w tym przykład Tindera.

7. Rada Y Combinator "do things that don't scale" i jej znaczenie w Dolinie Krzemowej.

8. Inwestorzy i ich rola w Dolinie Krzemowej, w tym ich strategia inwestycyjna i podejście do ryzyka.

9. Rekrutacja w Dolinie Krzemowej, w tym znaczenie doświadczenia i umiejętności w procesie rekrutacji.

10. Technologia i jej znaczenie w Dolinie Krzemowej, w tym pojęcie "product market fit" i jego ważność dla sukcesu firmy.

11. Wizerunek inwestorów w Dolinie Krzemowej, w tym ich podejście do pomysłów i założycieli firm.

12. Różnica między Doliną Krzemową a "big tech", w tym oddzielenie się tych dwóch światów.

Nota do redakcji pojawia się dwukrotnie:

* "Nota do redaktora warto by było zrobić taką sekcję z tymi pożekadłami z Doliny Krzemowej"

* "uwaga do redakcji bym jest już trochę mniej makabryczną metaforę"
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert len(result.items) == 12
    assert "Opis domu" in result.items[0]
    assert "big tech" in result.items[11]


def test_single_item_list_ignored():
    """Lists with only 1 item should be ignored (need at least 2)."""
    text = """
1. Only one item here

Some other text.
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, NoListFound)


def test_parenthesis_numbered_list():
    text = """
1) First item
2) Second item
3) Third item
"""
    result = extract_list(text, min_items=0, max_items=None)
    assert isinstance(result, ExtractedList)
    assert result.items == ("First item", "Second item", "Third item")
