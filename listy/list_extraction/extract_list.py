"""Main list extraction function that combines numbered and bullet list extraction."""

from .bullet import extract_bullet_lists
from .numbered import extract_numbered_lists
from .return_types import (
    AmbiguousLists,
    ExtractedList,
    ExtractionFailure,
    NoListFound,
    TooFewItems,
    TooManyItems,
)


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

    all_lists = [
        *extract_numbered_lists(text),
        *extract_bullet_lists(text),
    ]
    if len(all_lists) == 0:
        return NoListFound()

    lists_longest_first = sorted(all_lists, key=len, reverse=True)

    if ambiguity_threshold > 0:
        min_length = len(lists_longest_first[0]) * ambiguity_threshold
        candidates = [lst for lst in lists_longest_first if len(lst) >= min_length]
        if len(candidates) >= 2:
            return AmbiguousLists(candidates=tuple(tuple(lst) for lst in candidates))

    selected = lists_longest_first[0]

    if len(selected) < min_items:
        return TooFewItems(actual_count=len(selected))

    if max_items is not None and len(selected) > max_items:
        return TooManyItems(actual_count=len(selected))

    return ExtractedList(items=tuple(selected))
