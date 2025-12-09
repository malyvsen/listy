from itertools import groupby

from .line_classification import NumberedLine, OtherLine, classify_line


def extract_numbered_lists(text: str) -> list[list[str]]:
    """Extract all numbered lists from text, allowing blank lines between items."""
    lines = text.split("\n")
    classified = [classify_line(line) for line in lines]

    # Group by: numbered item, blank/whitespace, or other content
    # Split on "other content" only - blank lines don't break sequences
    groups = [
        [item for item in group if isinstance(item, NumberedLine)]
        for is_breaker, group in groupby(
            classified, key=lambda x: isinstance(x, OtherLine)
        )
        if not is_breaker
    ]

    return [
        items
        for group in groups
        for items in [_extract_valid_sequence(group)]
        if len(items) >= 2
    ]


def _extract_valid_sequence(numbered_items: list[NumberedLine]) -> list[str]:
    """Extract the longest valid 1-indexed sequence from numbered items."""
    if not numbered_items or numbered_items[0].number != 1:
        return []

    result = [numbered_items[0].content]
    expected = 2

    for item in numbered_items[1:]:
        if item.number == expected:
            result.append(item.content)
            expected += 1
        elif item.number == 1:
            # Restart sequence
            result = [item.content]
            expected = 2

    return result
