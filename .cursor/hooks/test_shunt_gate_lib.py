#!/usr/bin/env python3
"""Unit tests for shunt gate decisions (no network)."""

from __future__ import annotations

import os
import tempfile
import unittest

from shunt_gate_lib import (
    read_window_size,
    should_allow_read,
    should_allow_shell,
)


class TestReadWindow(unittest.TestCase):
    def test_full_file_over_cap_denied(self) -> None:
        d = should_allow_read(385, None, None, cap=350)
        self.assertFalse(d.allow)

    def test_bounded_limit_allowed(self) -> None:
        d = should_allow_read(385, 1, 100, cap=350)
        self.assertTrue(d.allow)

    def test_large_limit_denied(self) -> None:
        d = should_allow_read(385, 1, 400, cap=350)
        self.assertFalse(d.allow)

    def test_small_file_always_allowed(self) -> None:
        d = should_allow_read(100, None, None, cap=350)
        self.assertTrue(d.allow)

    def test_window_size(self) -> None:
        self.assertEqual(read_window_size(385, 1, None), 385)
        self.assertEqual(read_window_size(385, 10, 50), 50)


class TestShellGate(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.large = os.path.join(self.tmp, "large.txt")
        with open(self.large, "w", encoding="utf-8") as fh:
            fh.write("\n".join(f"line{i}" for i in range(400)))

    def test_cat_large_denied(self) -> None:
        d = should_allow_shell(f"cat {self.large}", self.tmp, cap=350)
        self.assertFalse(d.allow)

    def test_head_bounded_allowed(self) -> None:
        d = should_allow_shell(f"head -n 80 {self.large}", self.tmp, cap=350)
        self.assertTrue(d.allow)

    def test_grep_not_handled_by_dumper(self) -> None:
        d = should_allow_shell(f"grep line1 {self.large}", self.tmp, cap=350)
        self.assertTrue(d.allow)


if __name__ == "__main__":
    unittest.main()
