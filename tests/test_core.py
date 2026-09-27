"""Базовые автоматические проверки логики эмулятора (без GUI)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import parse_line
from vfs import resolve_path


class ParserTests(unittest.TestCase):
    """Проверки разбора команд."""

    def test_simple_command(self):
        command, args = parse_line("ls docs")
        self.assertEqual(command, "ls")
        self.assertEqual(args, ["docs"])

    def test_empty_line(self):
        command, args = parse_line("   ")
        self.assertIsNone(command)
        self.assertEqual(args, [])


class ResolvePathTests(unittest.TestCase):
    """Проверки построения пути внутри VFS."""

    def test_relative_move(self):
        self.assertEqual(resolve_path(["a", "b"], "c"), ["a", "b", "c"])

    def test_parent_move(self):
        self.assertEqual(resolve_path(["a", "b"], ".."), ["a"])

    def test_absolute_move(self):
        self.assertEqual(resolve_path(["a", "b"], "/x/y"), ["x", "y"])


if __name__ == "__main__":
    unittest.main()