from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedList:
    """Successfully extracted list items from text."""

    items: tuple[str, ...]


@dataclass(frozen=True)
class NoListFound:
    """No list was found in the text."""

    pass


@dataclass(frozen=True)
class AmbiguousLists:
    """Multiple lists of similar size were found, making selection ambiguous."""

    candidates: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class TooFewItems:
    """The extracted list has fewer items than required."""

    actual_count: int


@dataclass(frozen=True)
class TooManyItems:
    """The extracted list has more items than allowed."""

    actual_count: int


ExtractionFailure = NoListFound | AmbiguousLists | TooFewItems | TooManyItems
