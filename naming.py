u"""Generating unique, printable names."""

from __future__ import absolute_import
import unittest
import filtering


def number_printable(s, i):
    return u'{} ({})'.format(s, i)


def number_safe(s, i):
    return u'{}-{}'.format(s, i)


class UniqueNames(object):
    def __init__(self, normalising, numbering):
        self.normalising = normalising
        self.numbering = numbering
        self.keymap = {}
        self.used = set()

    def get(self, key):
        if key in self.keymap:
            return self.keymap[key]
        norm = self.normalising(key)
        i = None
        while True:
            if i is None:
                val = norm
            else:
                val = self.numbering(norm, i)
            if val not in self.used:
                self.used.add(val)
                self.keymap[key] = val
                return val
            i = 1 if i is None else i + 1


def printable_naming():
    return UniqueNames(filtering.printable, number_printable)


def safe_naming():
    return UniqueNames(filtering.safe, number_safe)


#### Unit tests


class TestUniqueNames(unittest.TestCase):
    def test_printable(self):
        u = printable_naming()
        for i in xrange(3):
            self.assertEqual(u.get(u'abc'), u'abc')
            self.assertEqual(u.get(u'123\n456'), u'123 456')
            self.assertEqual(u.get(u'abc\b'), u'abc (1)')
            self.assertEqual(u.get(u'a\bbc'), u'abc (2)')
            self.assertEqual(u.get(u'abc\n'), u'abc ')
            self.assertEqual(u.get(u'abc\r'), u'abc  (1)')
            self.assertEqual(u.get(u'abc\t'), u'abc  (2)')
            self.assertEqual(u.get(u'äbc'), u'äbc')
            self.assertEqual(u.get((u'abc',)), u'abc (3)')
            self.assertEqual(u.get(u'123 456'), u'123 456 (1)')
            self.assertEqual(u.get(u'123\t456'), u'123 456 (2)')
            self.assertEqual(u.get((u'123', u'456')), u'123 456 (3)')
            self.assertEqual(u.get(u''), u'')
            self.assertEqual(u.get(u'\b'), u' (1)')
            self.assertEqual(u.get(u'\0'), u' (2)')
            self.assertEqual(u.get(None), u' (3)')
            self.assertEqual(u.get(()), u' (4)')

    def test_safe(self):
        u = safe_naming()
        for i in xrange(3):
            self.assertEqual(u.get(u'abc'), u'abc')
            self.assertEqual(u.get(u'123\n456'), u'123-456')
            self.assertEqual(u.get(u'abc\b'), u'abc-1')
            self.assertEqual(u.get(u'a\bbc'), u'a-bc')
            self.assertEqual(u.get(u'abc\n'), u'abc-2')
            self.assertEqual(u.get(u'abc\r'), u'abc-3')
            self.assertEqual(u.get(u'abc\t'), u'abc-4')
            self.assertEqual(u.get(u'äbc'), u'abc-5')
            self.assertEqual(u.get((u'abc',)), u'abc-6')
            self.assertEqual(u.get(u'123 456'), u'123-456-1')
            self.assertEqual(u.get(u'123\t456'), u'123-456-2')
            self.assertEqual(u.get((u'123', u'456')), u'123-456-3')
            self.assertEqual(u.get(u''), u'-')
            self.assertEqual(u.get(u'\b'), u'--1')
            self.assertEqual(u.get(u'\0'), u'--2')
            self.assertEqual(u.get(None), u'--3')
            self.assertEqual(u.get(()), u'--4')


if __name__ == u'__main__':
    unittest.main()
