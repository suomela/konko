import re
import unittest


_space = re.compile('\s+')


def printable(s):
    if s.isprintable():
        return s
    return ''.join(c if c.isprintable() else ' ' for c in s if c.isprintable() or c.isspace())


def printable_nl(s):
    if s.isprintable():
        return s
    return ''.join(c if c.isprintable() or c == '\n' else ' ' for c in s if c.isprintable() or c.isspace())


def printable_compact(s):
    s = printable(s)
    return _space.sub(' ', s)


#### Unit tests


class TestTextFilters(unittest.TestCase):
    def test_printable(self):
        self.assertEqual(printable('abc'), 'abc')
        self.assertEqual(printable('abc äöå'), 'abc äöå')
        self.assertEqual(printable('abc\näöå'), 'abc äöå')
        self.assertEqual(printable('abc\täöå'), 'abc äöå')
        self.assertEqual(printable('abc\n\t äöå'), 'abc   äöå')
        self.assertEqual(printable('abc\b\0äöå'), 'abcäöå')

    def test_printable_nl(self):
        self.assertEqual(printable_nl('abc'), 'abc')
        self.assertEqual(printable_nl('abc äöå'), 'abc äöå')
        self.assertEqual(printable_nl('abc\näöå'), 'abc\näöå')
        self.assertEqual(printable_nl('abc\täöå'), 'abc äöå')
        self.assertEqual(printable_nl('abc\n\t äöå'), 'abc\n  äöå')
        self.assertEqual(printable_nl('abc\b\0äöå'), 'abcäöå')

    def test_printable_compact(self):
        self.assertEqual(printable_compact('abc'), 'abc')
        self.assertEqual(printable_compact('abc äöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\näöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\täöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\n\t äöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\b\0äöå'), 'abcäöå')


if __name__ == '__main__':
    unittest.main()
