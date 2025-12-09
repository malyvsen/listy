import re
from dataclasses import dataclass

NUMBERED_PATTERN = re.compile(r"^\s*(\d+)\s*[.)]\s*(.+)$")
BULLET_PATTERN = re.compile(r"^\s*[*\-•◦‣⁃]\s+(.+)$")


@dataclass(frozen=True)
class NumberedLine:
    """A numbered list item line."""

    number: int
    content: str


@dataclass(frozen=True)
class BulletLine:
    """A bullet list item line."""

    content: str


@dataclass(frozen=True)
class BlankLine:
    """A blank or whitespace-only line."""

    pass


@dataclass(frozen=True)
class OtherLine:
    """A line that is neither a list item nor blank."""

    pass


type LineClassification = NumberedLine | BulletLine | BlankLine | OtherLine


def classify_line(line: str) -> LineClassification:
    """Classify a line as numbered, bullet, blank, or other."""
    if match := NUMBERED_PATTERN.match(line):
        return NumberedLine(number=int(match.group(1)), content=match.group(2).strip())
    if match := BULLET_PATTERN.match(line):
        return BulletLine(content=match.group(1).strip())
    if not line.strip():
        return BlankLine()
    return OtherLine()
