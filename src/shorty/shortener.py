"""Core logic for removing comments and redundant whitespace from source code."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple
import re


@dataclass(frozen=True)
class LanguageStyle:
    """Configuration describing how to strip comments for a language."""

    block_comments: Sequence[Tuple[str, str]]
    line_comments: Sequence[str]


def _strip_block_comments(text: str, patterns: Sequence[Tuple[str, str]]) -> str:
    for start, end in patterns:
        if not start or not end:
            continue
        # Use a non-greedy regex to remove blocks across multiple lines.
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        text = pattern.sub("", text)
    return text


def _find_marker_outside_strings(line: str, marker: str) -> Optional[int]:
    """Return index of the marker outside of single or double quoted strings."""

    if not marker:
        return None

    marker_length = len(marker)
    in_single = False
    in_double = False
    escape = False

    i = 0
    while i <= len(line) - marker_length:
        ch = line[i]

        if ch == "\\" and (in_single or in_double):
            escape = not escape
            i += 1
            continue

        if ch == "'" and not in_double:
            if not escape:
                in_single = not in_single
            escape = False
            i += 1
            continue

        if ch == '"' and not in_single:
            if not escape:
                in_double = not in_double
            escape = False
            i += 1
            continue

        escape = False

        if not in_single and not in_double:
            if line.startswith(marker, i):
                # Avoid stripping URLs such as http:// or https://
                if marker == "//" and i > 0 and line[i - 1] == ':' and "//" in line[i - 1 : i + 2]:
                    i += marker_length
                    continue
                return i
        i += 1

    return None


def _strip_line_comments(text: str, markers: Sequence[str]) -> str:
    if not markers:
        return text

    processed_lines: List[str] = []
    for original_line in text.splitlines():
        line = original_line
        for marker in markers:
            index = _find_marker_outside_strings(line, marker)
            if index is not None:
                line = line[:index]
        processed_lines.append(line.rstrip())
    return "\n".join(processed_lines)


def _collapse_blank_lines(text: str) -> str:
    lines = text.splitlines()
    collapsed: List[str] = []
    for line in lines:
        if line.strip():
            collapsed.append(line.rstrip())
    result = "\n".join(collapsed).strip()
    if result:
        result += "\n"
    return result


LANGUAGE_STYLES: Dict[str, LanguageStyle] = {
    "c": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "cpp": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "c++": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "c#": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "java": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "javascript": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "js": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//",)),
    "php": LanguageStyle(block_comments=(("/*", "*/"),), line_comments=("//", "#")),
    "python": LanguageStyle(block_comments=(("\"\"\"", "\"\"\""), ("'''", "'''")), line_comments=("#",)),
    "html": LanguageStyle(block_comments=(("<!--", "-->"),), line_comments=()),
}


def resolve_language_style(language: Optional[str]) -> LanguageStyle:
    if language:
        key = language.lower()
        if key in LANGUAGE_STYLES:
            return LANGUAGE_STYLES[key]
    # Fallback combines common comment markers.
    combined_blocks: List[Tuple[str, str]] = [("/*", "*/"), ("<!--", "-->"), ("\"\"\"", "\"\"\""), ("'''", "'''")]
    combined_lines: List[str] = ["//", "#", "--"]
    return LanguageStyle(block_comments=combined_blocks, line_comments=combined_lines)


def shorten_code(text: str, language: Optional[str] = None) -> str:
    """Return a shortened version of *text* by removing comments and blank lines."""

    style = resolve_language_style(language)
    without_blocks = _strip_block_comments(text, style.block_comments)
    without_line = _strip_line_comments(without_blocks, style.line_comments)
    return _collapse_blank_lines(without_line)


__all__ = ["LanguageStyle", "shorten_code", "resolve_language_style"]
