from itertools import groupby

from .line_classification import BulletLine, OtherLine, classify_line


def extract_bullet_lists(text: str) -> list[list[str]]:
    """Extract all bullet-pointed lists from text, allowing blank lines between items."""
    lines = text.split("\n")
    classified = [classify_line(line) for line in lines]

    # Split on "other content" only - blank lines don't break sequences
    groups = [
        [item.content for item in group if isinstance(item, BulletLine)]
        for is_breaker, group in groupby(
            classified, key=lambda x: isinstance(x, OtherLine)
        )
        if not is_breaker
    ]

    return [group for group in groups if len(group) >= 2]
