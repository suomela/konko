# coding=utf-8
u"""Generating safe, printable string."""

import re
import string
import unicodedata
import unittest


_unsafe = re.compile(ur'[^a-z0-9]+')


def stringify(s):
    if s is None:
        return u''
    elif isinstance(s, unicode):
        return s
    else:
        return u' '.join(s)


def _isprintable(s):
    if s == '':
        return s
    a = min(s)
    b = max(s)
    return a >= ' ' and b <= '~'


def printable(s):
    s = stringify(s)
    if _isprintable(s):
        return s
    r = u''
    for c in s:
        if c.isspace():
            r += u' '
        elif unicodedata.category(c)[0] not in 'CZ':
            r += c
    return r


def printable_nl(s):
    s = stringify(s)
    if _isprintable(s):
        return s
    r = u''
    for c in s:
        if c == u'\n':
            r += c
        elif c.isspace():
            r += u' '
        elif unicodedata.category(c)[0] not in 'CZ':
            r += c
    return r



def printable_compact(s):
    s = printable(s)
    while True:
        x = s.replace(u'  ', u' ')
        if x == s:
            return x
        s = x


def safe(s):
    s = stringify(s)
    s = s.lower()
    s = unicodedata.normalize(u'NFKD', s)
    s = u''.join(c for c in s if unicodedata.category(c) not in (u'Mn',))
    s = _unsafe.sub(u'-', s)
    s = s.strip(u'-')
    if s == u'':
        s = u'-'
    return s


#### Unit tests


class TestTextFilters(unittest.TestCase):
    def test_printable(self):
        self.assertEqual(printable(None), u'')
        self.assertEqual(printable(u''), u'')
        self.assertEqual(printable(u'abc'), u'abc')
        self.assertEqual(printable(u'abc äöå'), u'abc äöå')
        self.assertEqual(printable(u'abc\näöå'), u'abc äöå')
        self.assertEqual(printable(u'abc\täöå'), u'abc äöå')
        self.assertEqual(printable(u'abc\n\t äöå'), u'abc   äöå')
        self.assertEqual(printable(u'abc\r\t äöå'), u'abc   äöå')
        self.assertEqual(printable(u'abc\b\0äöå'), u'abcäöå')
        self.assertEqual(printable(u'  abc  '), u'  abc  ')
        self.assertEqual(printable((u'abc', u'äöå')), u'abc äöå')
        self.assertEqual(printable([u'abc', u'äöå']), u'abc äöå')
        self.assertEqual(printable([u'abc']), u'abc')
        self.assertEqual(printable([]), u'')

    def test_printable_nl(self):
        self.assertEqual(printable_nl(None), u'')
        self.assertEqual(printable_nl(u''), u'')
        self.assertEqual(printable_nl(u'abc'), u'abc')
        self.assertEqual(printable_nl(u'abc äöå'), u'abc äöå')
        self.assertEqual(printable_nl(u'abc\näöå'), u'abc\näöå')
        self.assertEqual(printable_nl(u'abc\täöå'), u'abc äöå')
        self.assertEqual(printable_nl(u'abc\n\t äöå'), u'abc\n  äöå')
        self.assertEqual(printable_nl(u'abc\r\t äöå'), u'abc   äöå')
        self.assertEqual(printable_nl(u'abc\b\0äöå'), u'abcäöå')
        self.assertEqual(printable_nl(u'  abc  '), u'  abc  ')

    def test_printable_compact(self):
        self.assertEqual(printable_compact(None), u'')
        self.assertEqual(printable_compact(u''), u'')
        self.assertEqual(printable_compact(u'abc'), u'abc')
        self.assertEqual(printable_compact(u'abc äöå'), u'abc äöå')
        self.assertEqual(printable_compact(u'abc\näöå'), u'abc äöå')
        self.assertEqual(printable_compact(u'abc\täöå'), u'abc äöå')
        self.assertEqual(printable_compact(u'abc\n\t äöå'), u'abc äöå')
        self.assertEqual(printable_compact(u'abc\r\t äöå'), u'abc äöå')
        self.assertEqual(printable_compact(u'abc\b\0äöå'), u'abcäöå')
        self.assertEqual(printable_compact(u'  abc  '), u' abc ')

    def test_safe(self):
        # Always non-empty
        self.assertEqual(safe(None), u'-')
        self.assertEqual(safe(u''), u'-')
        self.assertEqual(safe(u'!#@'), u'-')
        self.assertEqual(safe(u'abc'), u'abc')
        self.assertEqual(safe(u'abc äöå'), u'abc-aoa')
        # Far from perfect
        self.assertEqual(safe(u'abc äöå àáâãā šś æß'), u'abc-aoa-aaaaa-ss')
        self.assertEqual(safe(u'abc\näöå'), u'abc-aoa')
        self.assertEqual(safe(u'abc\täöå'), u'abc-aoa')
        self.assertEqual(safe(u'abc\n\t äöå'), u'abc-aoa')
        self.assertEqual(safe(u'abc\r\t äöå'), u'abc-aoa')
        self.assertEqual(safe(u'abc\b\0äöå'), u'abc-aoa')
        self.assertEqual(safe(u'abc ABC 123 äöå'), u'abc-abc-123-aoa')
        self.assertEqual(safe(u' -_?!,. abc/ABC 123 - äöå '), u'abc-abc-123-aoa')
        self.assertEqual(safe((u'abc', u'äöå')), u'abc-aoa')
        self.assertEqual(safe([u'abc', u'äöå']), u'abc-aoa')
        self.assertEqual(safe([u'abc']), u'abc')
        self.assertEqual(safe([]), u'-')


if __name__ == u'__main__':
    unittest.main()
