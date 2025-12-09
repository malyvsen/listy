import re
from itertools import groupby

from .types import (
    AmbiguousLists,
    ExtractedList,
    ExtractionFailure,
    NoListFound,
    TooFewItems,
    TooManyItems,
)

NUMBERED_PATTERN = re.compile(r"^\s*(\d+)\s*[.)]\s*(.+)$")
BULLET_PATTERN = re.compile(r"^\s*[*\-•◦‣⁃]\s+(.+)$")


def extract_list(
    text: str,
    min_items: int,
    max_items: int | None,
    ambiguity_threshold: float = 0.7,
) -> ExtractedList | ExtractionFailure:
    """
    Extract list items from unstructured text.

    When multiple lists are found, picks the longest one unless there are
    ambiguous candidates (within the threshold ratio of the longest).
    """
    lists = sorted(_find_all_lists(text), key=len, reverse=True)

    if not lists:
        return NoListFound()

    if ambiguity_threshold > 0:
        min_length = len(lists[0]) * ambiguity_threshold
        candidates = [lst for lst in lists if len(lst) >= min_length]
        if len(candidates) >= 2:
            return AmbiguousLists(candidates=tuple(tuple(lst) for lst in candidates))

    selected = lists[0]

    if len(selected) < min_items:
        return TooFewItems(actual_count=len(selected))

    if max_items is not None and len(selected) > max_items:
        return TooManyItems(actual_count=len(selected))

    return ExtractedList(items=tuple(selected))


def _find_all_lists(text: str) -> list[list[str]]:
    """Find all numbered and bullet-pointed lists in the text."""
    return [
        *_extract_numbered_lists(text),
        *_extract_bullet_lists(text),
    ]


def _extract_numbered_lists(text: str) -> list[list[str]]:
    """Extract all numbered lists from text, allowing blank lines between items."""
    lines = text.split("\n")
    classified = [_classify_line(line) for line in lines]

    # Group by: numbered item, blank/whitespace, or other content
    # Split on "other content" only - blank lines don't break sequences
    groups = [
        [item for tag, item in group if tag == "numbered"]
        for is_breaker, group in groupby(classified, key=lambda x: x[0] == "other")
        if not is_breaker
    ]

    return [
        items
        for group in groups
        for items in [_extract_valid_sequence(group)]
        if len(items) >= 2
    ]


def _classify_line(line: str) -> tuple[str, tuple[int, str] | None]:
    """Classify a line as 'numbered', 'blank', or 'other'."""
    if match := NUMBERED_PATTERN.match(line):
        return ("numbered", (int(match.group(1)), match.group(2).strip()))
    if not line.strip():
        return ("blank", None)
    return ("other", None)


def _extract_valid_sequence(numbered_items: list[tuple[int, str]]) -> list[str]:
    """Extract the longest valid 1-indexed sequence from numbered items."""
    if not numbered_items or numbered_items[0][0] != 1:
        return []

    result = [numbered_items[0][1]]
    expected = 2

    for num, content in numbered_items[1:]:
        if num == expected:
            result.append(content)
            expected += 1
        elif num == 1:
            # Restart sequence
            result = [content]
            expected = 2

    return result


def _extract_bullet_lists(text: str) -> list[list[str]]:
    """Extract all bullet-pointed lists from text, allowing blank lines between items."""
    lines = text.split("\n")
    classified = [_classify_bullet_line(line) for line in lines]

    # Split on "other content" only - blank lines don't break sequences
    groups = [
        [item for tag, item in group if tag == "bullet"]
        for is_breaker, group in groupby(classified, key=lambda x: x[0] == "other")
        if not is_breaker
    ]

    return [group for group in groups if len(group) >= 2]


def _classify_bullet_line(line: str) -> tuple[str, str | None]:
    """Classify a line as 'bullet', 'blank', or 'other'."""
    if match := BULLET_PATTERN.match(line):
        return ("bullet", match.group(1).strip())
    if not line.strip():
        return ("blank", None)
    return ("other", None)
