#!/usr/bin/env python3
"""Safely normalize punctuation in Markdown prose without reserializing Markdown."""

from __future__ import annotations

import argparse
import codecs
import difflib
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
except ImportError as exc:  # pragma: no cover - exercised by the CLI environment
    raise SystemExit(
        "缺少 markdown-it-py。请运行: "
        "python -m pip install -r script/requirements.txt"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SKIPPED_DIRECTORIES = {".git", "node_modules", "labs", "site", "__pycache__"}
PROTECTED_BLOCK_TYPES = {"fence", "code_block", "html_block"}

MASK_NONE = 0
MASK_HIDDEN = 1
MASK_OPAQUE = 2
MASK_BLOCK = 3
MASK_HTML_OPEN = 4
MASK_HTML_CLOSE = 5

SIMPLE_REPLACEMENTS = {
    "，": ",",
    "、": ",",
    "；": ";",
    "：": ":",
    "？": "?",
    "！": "!",
}
OPEN_PARENS = {"（": "("}
CLOSE_PARENS = {"）": ")"}
OPEN_QUOTES = {"“": '"', "‘": '"', "「": '"', "『": '"'}
CLOSE_QUOTES = {"”": '"', "’": '"', "」": '"', "』": '"'}
TARGET_CHARACTERS = set(SIMPLE_REPLACEMENTS) | {
    "。",
    "（",
    "）",
    "“",
    "”",
    "‘",
    "’",
    "「",
    "」",
    "『",
    "』",
    "／",
}
FULLWIDTH_CLOSERS = set("）”’」』》】")
ASCII_BOUNDARY_PUNCTUATION = set(",.;:?!)]}")


class StructureChangedError(RuntimeError):
    """Raised when normalization changes the parsed Markdown structure."""


def configure_standard_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class FileEncoding:
    bom: bool


@dataclass(frozen=True)
class NormalizationResult:
    text: str
    replacements: int
    changed_lines: int


@dataclass(frozen=True)
class FileResult:
    path: Path
    original: str
    normalized: str
    replacements: int
    changed_lines: int

    @property
    def changed(self) -> bool:
        return self.original != self.normalized


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="只修改 Markdown 正文节点中的中文标点，并保护代码、公式和链接。"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[REPO_ROOT],
        help="要检查的 Markdown 文件或目录；默认检查整个仓库。",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="只检查；发现可修复内容时返回退出码 1（默认）。",
    )
    mode.add_argument(
        "--fix",
        action="store_true",
        help="原子写回高置信度修复。",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        type=Path,
        metavar="PATH",
        help="额外排除的文件或目录，可重复指定。",
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="显示统一差异。",
    )
    return parser.parse_args(argv)


def _line_offsets(text: str) -> tuple[list[str], list[int]]:
    lines = text.splitlines(keepends=True)
    if not lines and text:
        lines = [text]
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    return lines, offsets


def _mark(mask: bytearray, start: int, end: int, kind: int) -> None:
    start = max(0, start)
    end = min(len(mask), end)
    for index in range(start, end):
        if mask[index] in (MASK_NONE, MASK_HIDDEN):
            mask[index] = kind


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _run_length(text: str, index: int, character: str, end: int) -> int:
    cursor = index
    while cursor < end and text[cursor] == character:
        cursor += 1
    return cursor - index


def _mask_run_end(mask: bytearray, index: int, end: int) -> int:
    kind = mask[index]
    cursor = index + 1
    while cursor < end and mask[cursor] == kind:
        cursor += 1
    return cursor


def _is_han(character: str) -> bool:
    return (
        "\u3400" <= character <= "\u4dbf"
        or "\u4e00" <= character <= "\u9fff"
        or "\uf900" <= character <= "\ufaff"
    )


def _token_signature(tokens: Iterable[Token]) -> tuple[tuple[object, ...], ...]:
    signature: list[tuple[object, ...]] = []
    for token in tokens:
        children = tuple(
            (child.type, child.tag, child.nesting, child.markup)
            for child in (token.children or [])
            if child.type != "text"
        )
        signature.append(
            (token.type, token.tag, token.nesting, token.level, token.markup, children)
        )
    return tuple(signature)


class MarkdownPunctuationNormalizer:
    """Normalize prose while preserving the source representation of Markdown."""

    def __init__(self) -> None:
        self.markdown = MarkdownIt("commonmark", {"html": True})

    def normalize(
        self,
        text: str,
        *,
        validate_structure: bool = True,
        _single_pass: bool = False,
    ) -> NormalizationResult:
        if not text:
            return NormalizationResult(text=text, replacements=0, changed_lines=0)

        original_tokens = self.markdown.parse(text)
        lines, offsets = _line_offsets(text)
        editable = bytearray(len(text))
        mask = bytearray(len(text))
        inline_spans: list[tuple[int, int]] = []

        for token in original_tokens:
            if token.map is None:
                continue
            start_line, end_line = token.map
            start = offsets[min(start_line, len(lines))]
            end = offsets[min(end_line, len(lines))]
            if token.type == "inline":
                inline_spans.append((start, end))
                editable[start:end] = b"\x01" * (end - start)
            elif token.type in PROTECTED_BLOCK_TYPES:
                _mark(mask, start, end, MASK_BLOCK)

        self._protect_front_matter(lines, offsets, mask)
        self._protect_directive_ranges(lines, offsets, mask)
        self._protect_reference_definitions(lines, offsets, mask)

        for start, end in inline_spans:
            self._protect_code_spans(text, start, end, mask)
            self._protect_math(text, start, end, mask)
            self._protect_links(text, start, end, mask)
            self._protect_angle_constructs(text, start, end, mask)

        open_markup = bytearray(len(text))
        close_markup = bytearray(len(text))
        for start, end in inline_spans:
            self._pair_markup(text, start, end, mask, open_markup, close_markup)

        replacements: dict[int, str] = {}
        removals: set[int] = set()
        insertions: set[int] = set()
        replacement_count = 0

        for start, end in inline_spans:
            index = start
            while index < end:
                character = text[index]
                if not editable[index] or mask[index] != MASK_NONE:
                    index += 1
                    continue

                if character in SIMPLE_REPLACEMENTS:
                    replacements[index] = SIMPLE_REPLACEMENTS[character]
                    replacement_count += 1
                    self._remove_space_before(text, index, start, removals)
                    self._ensure_space_after(
                        text, index, end, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                elif character == "。":
                    boundary = self._following_boundary(
                        text, index + 1, end, mask, open_markup, close_markup
                    )
                    self._remove_space_before(text, index, start, removals)
                    if (
                        boundary[0]
                        and not boundary[4]
                        and not self._is_boundary_punctuation(text, boundary[1], mask)
                    ):
                        replacements[index] = ","
                        self._apply_following_spacing(boundary, removals, insertions)
                    else:
                        replacements[index] = ""
                        if not boundary[2]:
                            removals.update(boundary[3])
                        if (
                            boundary[0]
                            and boundary[4]
                            and not boundary[2]
                            and not self._is_boundary_punctuation(text, boundary[1], mask)
                        ):
                            insertions.add(boundary[1])
                    replacement_count += 1
                elif character in OPEN_PARENS:
                    replacements[index] = OPEN_PARENS[character]
                    replacement_count += 1
                    self._ensure_space_before(
                        text, index, start, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                    self._remove_space_after(text, index, end, removals)
                elif character in CLOSE_PARENS:
                    replacements[index] = CLOSE_PARENS[character]
                    replacement_count += 1
                    self._remove_space_before(text, index, start, removals)
                    self._ensure_space_after(
                        text, index, end, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                elif character in OPEN_QUOTES:
                    replacements[index] = OPEN_QUOTES[character]
                    replacement_count += 1
                    self._ensure_space_before(
                        text, index, start, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                    self._remove_space_after(text, index, end, removals)
                elif character in CLOSE_QUOTES:
                    replacements[index] = CLOSE_QUOTES[character]
                    replacement_count += 1
                    self._remove_space_before(text, index, start, removals)
                    self._ensure_space_after(
                        text, index, end, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                elif character == "／":
                    replacements[index] = "/"
                    replacement_count += 1
                    self._ensure_space_before(
                        text, index, start, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                    self._ensure_space_after(
                        text, index, end, mask, open_markup, close_markup,
                        removals, insertions,
                    )
                elif character in ",;:?!":
                    previous = self._previous_plain_character(text, index, start, mask)
                    following = self._next_plain_character(text, index + 1, end, mask)
                    follows_word = bool(
                        following and following not in ASCII_BOUNDARY_PUNCTUATION
                    )
                    if (following and _is_han(following)) or (
                        previous and _is_han(previous) and follows_word
                    ):
                        self._remove_space_before(text, index, start, removals)
                        self._ensure_space_after(
                            text, index, end, mask, open_markup, close_markup,
                            removals, insertions,
                        )
                elif character == "(":
                    previous = self._previous_plain_character(text, index, start, mask)
                    if previous and _is_han(previous):
                        self._ensure_space_before(
                            text, index, start, mask, open_markup, close_markup,
                            removals, insertions,
                        )
                        self._remove_space_after(text, index, end, removals)
                elif character == ")":
                    following = self._next_plain_character(text, index + 1, end, mask)
                    if following and _is_han(following):
                        self._remove_space_before(text, index, start, removals)
                        self._ensure_space_after(
                            text, index, end, mask, open_markup, close_markup,
                            removals, insertions,
                        )
                index += 1

        normalized = self._apply_edits(text, replacements, removals, insertions)
        changed_lines = self._count_changed_lines(text, normalized)

        if normalized != text and not _single_pass:
            for _ in range(32):
                follow_up = self.normalize(
                    normalized,
                    validate_structure=False,
                    _single_pass=True,
                )
                replacement_count += follow_up.replacements
                if follow_up.text == normalized:
                    break
                normalized = follow_up.text
            else:  # pragma: no cover - protects against a future oscillating rule
                raise RuntimeError("标点归一化在 32 轮内未收敛")
            changed_lines = self._count_changed_lines(text, normalized)

        if normalized != text and validate_structure:
            normalized_tokens = self.markdown.parse(normalized)
            if _token_signature(original_tokens) != _token_signature(normalized_tokens):
                raise StructureChangedError("归一化会改变 Markdown 解析结构，已拒绝写入")

        return NormalizationResult(
            text=normalized,
            replacements=replacement_count,
            changed_lines=changed_lines,
        )

    @staticmethod
    def _protect_front_matter(
        lines: list[str], offsets: list[int], mask: bytearray
    ) -> None:
        if not lines or lines[0].rstrip("\r\n") != "---":
            return
        for line_number in range(1, len(lines)):
            if lines[line_number].rstrip("\r\n") in {"---", "..."}:
                _mark(mask, offsets[0], offsets[line_number + 1], MASK_BLOCK)
                return

    @staticmethod
    def _protect_reference_definitions(
        lines: list[str], offsets: list[int], mask: bytearray
    ) -> None:
        pattern = re.compile(r"^ {0,3}\[[^\]\r\n]+\]:")
        for line_number, line in enumerate(lines):
            if pattern.match(line):
                _mark(mask, offsets[line_number], offsets[line_number + 1], MASK_HIDDEN)

    @staticmethod
    def _protect_directive_ranges(
        lines: list[str], offsets: list[int], mask: bytearray
    ) -> None:
        disabled_at: int | None = None
        for line_number, line in enumerate(lines):
            directive = line.strip()
            if directive == "<!-- punctuation: off -->" and disabled_at is None:
                disabled_at = line_number
            elif directive == "<!-- punctuation: on -->" and disabled_at is not None:
                _mark(mask, offsets[disabled_at], offsets[line_number + 1], MASK_BLOCK)
                disabled_at = None
        if disabled_at is not None:
            _mark(mask, offsets[disabled_at], offsets[-1], MASK_BLOCK)

    @staticmethod
    def _protect_code_spans(
        text: str, start: int, end: int, mask: bytearray
    ) -> None:
        index = start
        while index < end:
            if mask[index] != MASK_NONE or text[index] != "`" or _is_escaped(text, index):
                index += 1
                continue
            length = _run_length(text, index, "`", end)
            cursor = index + length
            closing = None
            while cursor < end:
                if mask[cursor] == MASK_BLOCK:
                    break
                if text[cursor] == "`" and not _is_escaped(text, cursor):
                    candidate_length = _run_length(text, cursor, "`", end)
                    if candidate_length == length:
                        closing = cursor + length
                        break
                    cursor += candidate_length
                else:
                    cursor += 1
            if closing is None:
                index += length
                continue
            _mark(mask, index, closing, MASK_OPAQUE)
            index = closing

    @staticmethod
    def _protect_math(text: str, start: int, end: int, mask: bytearray) -> None:
        index = start
        while index < end:
            if mask[index] != MASK_NONE:
                index += 1
                continue

            opener = None
            closer = None
            if text.startswith("\\(", index) and not _is_escaped(text, index):
                opener, closer = "\\(", "\\)"
            elif text.startswith("\\[", index) and not _is_escaped(text, index):
                opener, closer = "\\[", "\\]"
            elif text[index] == "$" and not _is_escaped(text, index):
                run = _run_length(text, index, "$", end)
                if run >= 2:
                    opener = closer = "$$"
                elif index + 1 < end and not text[index + 1].isspace():
                    opener = closer = "$"

            if opener is None or closer is None:
                index += 1
                continue

            cursor = index + len(opener)
            closing = None
            while cursor < end:
                if mask[cursor] != MASK_NONE:
                    cursor += 1
                    continue
                if text.startswith(closer, cursor) and not _is_escaped(text, cursor):
                    closing = cursor + len(closer)
                    break
                cursor += 1
            if closing is None:
                index += len(opener)
                continue
            _mark(mask, index, closing, MASK_OPAQUE)
            index = closing

    @staticmethod
    def _protect_links(text: str, start: int, end: int, mask: bytearray) -> None:
        index = start
        while index < end:
            if mask[index] != MASK_NONE or text[index] != "]":
                index += 1
                continue

            cursor = index + 1
            while cursor < end and text[cursor] in " \t":
                cursor += 1
            if cursor >= end or text[cursor] not in "([":
                index += 1
                continue

            opener = text[cursor]
            closer = ")" if opener == "(" else "]"
            depth = 0
            quote = None
            closing = None
            scan = cursor
            while scan < end:
                if mask[scan] != MASK_NONE:
                    scan += 1
                    continue
                character = text[scan]
                if character in "\r\n" and opener == "[":
                    break
                if quote:
                    if character == quote and not _is_escaped(text, scan):
                        quote = None
                elif character in "\"'":
                    quote = character
                elif character == opener and not _is_escaped(text, scan):
                    depth += 1
                elif character == closer and not _is_escaped(text, scan):
                    depth -= 1
                    if depth == 0:
                        closing = scan + 1
                        break
                scan += 1
            if closing is None:
                index += 1
                continue
            _mark(mask, cursor, closing, MASK_HIDDEN)
            index = closing

    @staticmethod
    def _protect_angle_constructs(
        text: str, start: int, end: int, mask: bytearray
    ) -> None:
        index = start
        while index < end:
            if mask[index] != MASK_NONE or text[index] != "<":
                index += 1
                continue
            line_end = min(
                (position for position in (text.find("\n", index, end), end) if position != -1),
                default=end,
            )
            cursor = index + 1
            quote = None
            closing = None
            while cursor < line_end:
                character = text[cursor]
                if quote:
                    if character == quote and not _is_escaped(text, cursor):
                        quote = None
                elif character in "\"'":
                    quote = character
                elif character == ">":
                    closing = cursor + 1
                    break
                cursor += 1
            if closing is None:
                index += 1
                continue

            inside = text[index + 1 : closing - 1].strip()
            if re.match(r"(?:https?://|mailto:)", inside, re.IGNORECASE):
                kind = MASK_OPAQUE
            elif inside.startswith("/"):
                kind = MASK_HTML_CLOSE
            else:
                kind = MASK_HTML_OPEN
            _mark(mask, index, closing, kind)
            index = closing

    @staticmethod
    def _pair_markup(
        text: str,
        start: int,
        end: int,
        mask: bytearray,
        open_markup: bytearray,
        close_markup: bytearray,
    ) -> None:
        stacks: dict[str, list[tuple[int, int]]] = {}
        bracket_stack: list[int] = []
        index = start
        while index < end:
            if mask[index] != MASK_NONE:
                index = _mask_run_end(mask, index, end)
                continue
            character = text[index]
            if character in "*_~" and not _is_escaped(text, index):
                length = _run_length(text, index, character, end)
                marker = character * length
                stack = stacks.setdefault(marker, [])
                if stack:
                    opening, opening_length = stack.pop()
                    open_markup[opening : opening + opening_length] = b"\x01" * opening_length
                    close_markup[index : index + length] = b"\x01" * length
                else:
                    stack.append((index, length))
                index += length
                continue
            if character == "[" and not _is_escaped(text, index):
                bracket_stack.append(index)
            elif character == "]" and bracket_stack and not _is_escaped(text, index):
                opening = bracket_stack.pop()
                open_markup[opening] = 1
                close_markup[index] = 1
            index += 1

    @staticmethod
    def _previous_plain_character(
        text: str, index: int, start: int, mask: bytearray
    ) -> str | None:
        cursor = index - 1
        while cursor >= start:
            if text[cursor] in " \t\r\n":
                cursor -= 1
                continue
            if mask[cursor] == MASK_OPAQUE:
                return "字"
            if mask[cursor] != MASK_NONE:
                cursor -= 1
                continue
            return text[cursor]
        return None

    @staticmethod
    def _next_plain_character(
        text: str, index: int, end: int, mask: bytearray
    ) -> str | None:
        cursor = index
        while cursor < end:
            if text[cursor] in " \t\r\n":
                cursor += 1
                continue
            if mask[cursor] == MASK_OPAQUE:
                return "字"
            if mask[cursor] != MASK_NONE:
                cursor += 1
                continue
            return text[cursor]
        return None

    @staticmethod
    def _remove_space_before(
        text: str, index: int, start: int, removals: set[int]
    ) -> None:
        cursor = index - 1
        spaces: list[int] = []
        while cursor >= start and text[cursor] in " \t":
            spaces.append(cursor)
            cursor -= 1
        if cursor >= start and text[cursor] not in "\r\n":
            removals.update(spaces)

    @staticmethod
    def _remove_space_after(
        text: str, index: int, end: int, removals: set[int]
    ) -> None:
        cursor = index + 1
        while cursor < end and text[cursor] in " \t":
            removals.add(cursor)
            cursor += 1

    def _ensure_space_before(
        self,
        text: str,
        index: int,
        start: int,
        mask: bytearray,
        open_markup: bytearray,
        close_markup: bytearray,
        removals: set[int],
        insertions: set[int],
    ) -> None:
        cursor = index - 1
        spaces: list[int] = []
        while cursor >= start and text[cursor] in " \t":
            spaces.append(cursor)
            cursor -= 1
        if cursor < start or text[cursor] in "\r\n":
            return
        if open_markup[cursor]:
            return
        if mask[cursor] == MASK_OPAQUE:
            needs_space = True
        elif mask[cursor] != MASK_NONE:
            needs_space = False
        else:
            character = text[cursor]
            needs_space = (
                character.isalnum()
                or _is_han(character)
                or bool(close_markup[cursor])
                or character in {")", "]", "}", '"', "'"}
            )
        if needs_space:
            removals.update(spaces)
            insertions.add(index)

    def _ensure_space_after(
        self,
        text: str,
        index: int,
        end: int,
        mask: bytearray,
        open_markup: bytearray,
        close_markup: bytearray,
        removals: set[int],
        insertions: set[int],
    ) -> None:
        boundary = self._following_boundary(
            text, index + 1, end, mask, open_markup, close_markup
        )
        if not boundary[0] or self._is_boundary_punctuation(text, boundary[1], mask):
            if not boundary[2]:
                removals.update(boundary[3])
            return
        self._apply_following_spacing(boundary, removals, insertions)

    @staticmethod
    def _apply_following_spacing(
        boundary: tuple[bool, int, bool, tuple[int, ...], bool],
        removals: set[int],
        insertions: set[int],
    ) -> None:
        _, position, crossed_newline, spaces, _ = boundary
        if crossed_newline:
            return
        removals.update(spaces)
        insertions.add(position)

    @staticmethod
    def _following_boundary(
        text: str,
        index: int,
        end: int,
        mask: bytearray,
        open_markup: bytearray,
        close_markup: bytearray,
    ) -> tuple[bool, int, bool, tuple[int, ...], bool]:
        cursor = index
        crossed_newline = False
        crossed_closer = False
        removable_spaces: list[int] = []
        while cursor < end:
            kind = mask[cursor]
            if kind in (MASK_BLOCK,):
                return False, cursor, crossed_newline, tuple(removable_spaces), crossed_closer
            if kind in (MASK_HIDDEN, MASK_HTML_CLOSE):
                if kind == MASK_HTML_CLOSE:
                    crossed_closer = True
                run_end = _mask_run_end(mask, cursor, end)
                if "\n" in text[cursor:run_end] or "\r" in text[cursor:run_end]:
                    crossed_newline = True
                cursor = run_end
                continue
            if kind in (MASK_OPAQUE, MASK_HTML_OPEN):
                return True, cursor, crossed_newline, tuple(removable_spaces), crossed_closer

            character = text[cursor]
            if character in " \t":
                removable_spaces.append(cursor)
                cursor += 1
                continue
            if character in "\r\n":
                crossed_newline = True
                cursor += 1
                continue
            if close_markup[cursor] or character in FULLWIDTH_CLOSERS or character in ")]}":
                crossed_closer = True
                cursor += 1
                continue
            if open_markup[cursor]:
                return True, cursor, crossed_newline, tuple(removable_spaces), crossed_closer
            return True, cursor, crossed_newline, tuple(removable_spaces), crossed_closer
        return False, end, crossed_newline, tuple(removable_spaces), crossed_closer

    @staticmethod
    def _is_boundary_punctuation(text: str, index: int, mask: bytearray) -> bool:
        if index >= len(text) or mask[index] in (MASK_OPAQUE, MASK_HTML_OPEN):
            return False
        return text[index] in ASCII_BOUNDARY_PUNCTUATION or text[index] in TARGET_CHARACTERS

    @staticmethod
    def _apply_edits(
        text: str,
        replacements: dict[int, str],
        removals: set[int],
        insertions: set[int],
    ) -> str:
        output: list[str] = []
        for index, character in enumerate(text):
            if index in insertions:
                if not output or not output[-1].endswith((" ", "\t", "\r", "\n")):
                    output.append(" ")
            if index in removals:
                continue
            output.append(replacements.get(index, character))
        if len(text) in insertions:
            output.append(" ")
        return "".join(output)

    @staticmethod
    def _count_changed_lines(original: str, normalized: str) -> int:
        original_lines = original.splitlines()
        normalized_lines = normalized.splitlines()
        return sum(
            left != right
            for left, right in zip(original_lines, normalized_lines, strict=True)
        )


def read_utf8(path: Path) -> tuple[str, FileEncoding]:
    data = path.read_bytes()
    bom = data.startswith(codecs.BOM_UTF8)
    if bom:
        data = data[len(codecs.BOM_UTF8) :]
    try:
        return data.decode("utf-8"), FileEncoding(bom=bom)
    except UnicodeDecodeError as exc:
        raise ValueError(f"不是有效的 UTF-8 文件: {path}") from exc


def write_utf8_atomic(path: Path, text: str, encoding: FileEncoding) -> None:
    payload = text.encode("utf-8")
    if encoding.bom:
        payload = codecs.BOM_UTF8 + payload
    mode = path.stat().st_mode
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        ) as temporary:
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.chmod(temporary_name, stat.S_IMODE(mode))
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def collect_markdown_files(paths: Sequence[Path], excludes: Sequence[Path]) -> list[Path]:
    excluded = [_resolved(path if path.is_absolute() else REPO_ROOT / path) for path in excludes]

    def is_excluded(path: Path) -> bool:
        resolved = _resolved(path)
        return any(resolved == item or item in resolved.parents for item in excluded)

    files: set[Path] = set()
    for input_path in paths:
        path = _resolved(input_path if input_path.is_absolute() else Path.cwd() / input_path)
        if path.is_file():
            if path.suffix.lower() == ".md" and not is_excluded(path):
                files.add(path)
            continue
        if not path.is_dir():
            raise FileNotFoundError(f"路径不存在: {input_path}")
        for candidate in path.rglob("*.md"):
            if any(part in SKIPPED_DIRECTORIES for part in candidate.parts):
                continue
            if not is_excluded(candidate):
                files.add(candidate.resolve())
    return sorted(files, key=lambda item: str(item).casefold())


def normalize_file(path: Path, normalizer: MarkdownPunctuationNormalizer) -> tuple[FileResult, FileEncoding]:
    original, encoding = read_utf8(path)
    normalized = normalizer.normalize(original)
    return (
        FileResult(
            path=path,
            original=original,
            normalized=normalized.text,
            replacements=normalized.replacements,
            changed_lines=normalized.changed_lines,
        ),
        encoding,
    )


def print_diff(result: FileResult) -> None:
    relative = result.path.relative_to(REPO_ROOT) if result.path.is_relative_to(REPO_ROOT) else result.path
    diff = difflib.unified_diff(
        result.original.splitlines(keepends=True),
        result.normalized.splitlines(keepends=True),
        fromfile=str(relative),
        tofile=str(relative),
    )
    sys.stdout.writelines(diff)


def main(argv: Sequence[str] | None = None) -> int:
    configure_standard_streams()
    args = parse_args(argv)
    excludes: list[Path] = list(args.exclude)

    try:
        files = collect_markdown_files(args.paths, excludes)
    except (FileNotFoundError, OSError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    normalizer = MarkdownPunctuationNormalizer()
    changed_files = 0
    changed_lines = 0
    replacements = 0
    errors = 0

    for path in files:
        try:
            result, encoding = normalize_file(path, normalizer)
        except (OSError, ValueError, StructureChangedError) as exc:
            print(f"错误: {path}: {exc}", file=sys.stderr)
            errors += 1
            continue
        if not result.changed:
            continue

        changed_files += 1
        changed_lines += result.changed_lines
        replacements += result.replacements
        relative = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        action = "Fixed" if args.fix else "Would change"
        print(f"{action}: {relative} ({result.changed_lines} lines)")
        if args.show_diff:
            print_diff(result)
        if args.fix:
            try:
                write_utf8_atomic(path, result.normalized, encoding)
            except OSError as exc:
                print(f"错误: 无法写入 {path}: {exc}", file=sys.stderr)
                errors += 1

    print(
        f"Checked {len(files)} files; {changed_files} files, "
        f"{changed_lines} lines, {replacements} target characters need changes"
    )
    if errors:
        return 2
    if changed_files and not args.fix:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
