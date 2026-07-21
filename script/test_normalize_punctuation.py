from __future__ import annotations

import codecs
import tempfile
import unittest
from pathlib import Path

from script.normalize_punctuation import (
    MarkdownPunctuationNormalizer,
    read_utf8,
    write_utf8_atomic,
)


class MarkdownPunctuationNormalizerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.normalizer = MarkdownPunctuationNormalizer()

    def assert_normalized(self, source: str, expected: str) -> None:
        first = self.normalizer.normalize(source).text
        second = self.normalizer.normalize(first).text
        self.assertEqual(first, expected)
        self.assertEqual(second, expected, "归一化必须幂等")

    def test_nested_list_and_basic_punctuation(self) -> None:
        self.assert_normalized(
            "- 父项\n    - 子项，内容。\n",
            "- 父项\n    - 子项, 内容\n",
        )

    def test_line_end_punctuation_preserves_following_indentation(self) -> None:
        self.assert_normalized(
            "- 主题涵盖：  \n        - 子项（细节）。\n",
            "- 主题涵盖:  \n        - 子项 (细节)\n",
        )

    def test_emphasis_quotes_parentheses_and_terminal_period(self) -> None:
        self.assert_normalized(
            "**“重点，内容。”** 后续。\n\n它“附近”的数据。\n\n甲（乙，丙）。\n",
            '**"重点, 内容"** 后续\n\n它 "附近" 的数据\n\n甲 (乙, 丙)\n',
        )

    def test_removed_period_exposes_a_parenthesis_boundary(self) -> None:
        self.assert_normalized(
            "甲。（乙。）丙。\n",
            "甲 (乙) 丙\n",
        )

    def test_period_before_inline_code_is_stable(self) -> None:
        self.assert_normalized(
            "前向声明可以节省重新编译。 `#include` 可能导致变化。\n",
            "前向声明可以节省重新编译, `#include` 可能导致变化\n",
        )

    def test_fenced_indented_and_blockquote_code_are_protected(self) -> None:
        source = (
            "正文，内容。\n"
            "```py\n代码，内容。\n```\n"
            "~~~py\n代码，内容。\n~~~\n"
            "    缩进代码，内容。\n"
            "> ```py\n> 引用代码，内容。\n> ```\n"
            "> 引用正文，内容。\n"
        )
        expected = (
            "正文, 内容\n"
            "```py\n代码，内容。\n```\n"
            "~~~py\n代码，内容。\n~~~\n"
            "    缩进代码，内容。\n"
            "> ```py\n> 引用代码，内容。\n> ```\n"
            "> 引用正文, 内容\n"
        )
        self.assert_normalized(source, expected)

    def test_inline_code_math_links_html_and_front_matter_are_protected(self) -> None:
        source = (
            "---\n"
            "title: 中文，标题。\n"
            "---\n"
            "文字， ``代码，`x` ``，结束。\n\n"
            "公式 $a，b$ 不改，正文。\n\n"
            "[中文，说明](https://example.com/（x）)。\n\n"
            '<span title="中，文">正文，内容。</span>\n'
        )
        expected = (
            "---\n"
            "title: 中文，标题。\n"
            "---\n"
            "文字, ``代码，`x` ``, 结束\n\n"
            "公式 $a，b$ 不改, 正文\n\n"
            "[中文, 说明](https://example.com/（x）)\n\n"
            '<span title="中，文">正文, 内容</span>\n'
        )
        self.assert_normalized(source, expected)

    def test_soft_wrapped_paragraph_uses_comma_before_next_line(self) -> None:
        self.assert_normalized("第一句。\n第二行。\n", "第一句,\n第二行\n")

    def test_explicit_exception_directive(self) -> None:
        source = (
            "正文，内容。\n\n"
            "<!-- punctuation: off -->\n"
            "保留，原样。\n"
            "<!-- punctuation: on -->\n\n"
            "继续，处理。\n"
        )
        expected = (
            "正文, 内容\n\n"
            "<!-- punctuation: off -->\n"
            "保留，原样。\n"
            "<!-- punctuation: on -->\n\n"
            "继续, 处理\n"
        )
        self.assert_normalized(source, expected)

    def test_existing_ascii_spacing_is_normalized_conservatively(self) -> None:
        self.assert_normalized(
            "中文,中文\n中文 : 内容\n中文(内容)后续\n$S_1$, ..., $S_k$\n",
            "中文, 中文\n中文: 内容\n中文 (内容) 后续\n$S_1$, ..., $S_k$\n",
        )

    def test_file_io_preserves_bom_crlf_and_final_newline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_bytes(codecs.BOM_UTF8 + "正文，内容。\r\n".encode("utf-8"))
            source, encoding = read_utf8(path)
            normalized = self.normalizer.normalize(source).text
            write_utf8_atomic(path, normalized, encoding)
            self.assertEqual(
                path.read_bytes(),
                codecs.BOM_UTF8 + "正文, 内容\r\n".encode("utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
