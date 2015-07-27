"""Generating safe, printable string."""

import re
import unicodedata
import unittest


_space = re.compile(r'\s+')
_unsafe = re.compile(r'[^a-z0-9]+')


def stringify(s):
    if s is None:
        return ''
    elif isinstance(s, str):
        return s
    else:
        return ' '.join(s)


def printable(s):
    s = stringify(s)
    if s.isprintable():
        return s
    return ''.join(c if c.isprintable() else ' ' for c in s if c.isprintable() or c.isspace())


def printable_nl(s):
    s = stringify(s)
    if s.isprintable():
        return s
    return ''.join(c if c.isprintable() or c == '\n' else ' ' for c in s if c.isprintable() or c.isspace())


def printable_compact(s):
    s = printable(s)
    return _space.sub(' ', s)


def safe(s):
    s = stringify(s)
    s = s.lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if unicodedata.category(c) not in ('Mn'))
    s = _unsafe.sub('-', s)
    s = s.strip('-')
    if s == '':
        s = '-'
    return s


#### Unit tests


class TestTextFilters(unittest.TestCase):
    def test_printable(self):
        self.assertEqual(printable(None), '')
        self.assertEqual(printable(''), '')
        self.assertEqual(printable('abc'), 'abc')
        self.assertEqual(printable('abc äöå'), 'abc äöå')
        self.assertEqual(printable('abc\näöå'), 'abc äöå')
        self.assertEqual(printable('abc\täöå'), 'abc äöå')
        self.assertEqual(printable('abc\n\t äöå'), 'abc   äöå')
        self.assertEqual(printable('abc\r\t äöå'), 'abc   äöå')
        self.assertEqual(printable('abc\b\0äöå'), 'abcäöå')
        self.assertEqual(printable('  abc  '), '  abc  ')
        self.assertEqual(printable(('abc', 'äöå')), 'abc äöå')
        self.assertEqual(printable(['abc', 'äöå']), 'abc äöå')
        self.assertEqual(printable(['abc']), 'abc')
        self.assertEqual(printable([]), '')

    def test_printable_nl(self):
        self.assertEqual(printable_nl(None), '')
        self.assertEqual(printable_nl(''), '')
        self.assertEqual(printable_nl('abc'), 'abc')
        self.assertEqual(printable_nl('abc äöå'), 'abc äöå')
        self.assertEqual(printable_nl('abc\näöå'), 'abc\näöå')
        self.assertEqual(printable_nl('abc\täöå'), 'abc äöå')
        self.assertEqual(printable_nl('abc\n\t äöå'), 'abc\n  äöå')
        self.assertEqual(printable_nl('abc\r\t äöå'), 'abc   äöå')
        self.assertEqual(printable_nl('abc\b\0äöå'), 'abcäöå')
        self.assertEqual(printable_nl('  abc  '), '  abc  ')

    def test_printable_compact(self):
        self.assertEqual(printable_compact(None), '')
        self.assertEqual(printable_compact(''), '')
        self.assertEqual(printable_compact('abc'), 'abc')
        self.assertEqual(printable_compact('abc äöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\näöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\täöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\n\t äöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\r\t äöå'), 'abc äöå')
        self.assertEqual(printable_compact('abc\b\0äöå'), 'abcäöå')
        self.assertEqual(printable_compact('  abc  '), ' abc ')

    def test_safe(self):
        # Always non-empty
        self.assertEqual(safe(None), '-')
        self.assertEqual(safe(''), '-')
        self.assertEqual(safe('!#@'), '-')
        self.assertEqual(safe('abc'), 'abc')
        self.assertEqual(safe('abc äöå'), 'abc-aoa')
        # Far from perfect
        self.assertEqual(safe('abc äöå àáâãā šś æß'), 'abc-aoa-aaaaa-ss')
        self.assertEqual(safe('abc\näöå'), 'abc-aoa')
        self.assertEqual(safe('abc\täöå'), 'abc-aoa')
        self.assertEqual(safe('abc\n\t äöå'), 'abc-aoa')
        self.assertEqual(safe('abc\r\t äöå'), 'abc-aoa')
        self.assertEqual(safe('abc\b\0äöå'), 'abc-aoa')
        self.assertEqual(safe('abc ABC 123 äöå'), 'abc-abc-123-aoa')
        self.assertEqual(safe(' -_?!,. abc/ABC 123 - äöå '), 'abc-abc-123-aoa')
        self.assertEqual(safe(('abc', 'äöå')), 'abc-aoa')
        self.assertEqual(safe(['abc', 'äöå']), 'abc-aoa')
        self.assertEqual(safe(['abc']), 'abc')
        self.assertEqual(safe([]), '-')


if __name__ == '__main__':
    unittest.main()
