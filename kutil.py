u"""Miscellaneous utility functions."""

from __future__ import absolute_import
import unittest
import glob
import os
import re
import sys


def exception_exit(msg):
    t, v, tb = sys.exc_info()
    print >>sys.stderr, u'{}.{}: {}'.format(t.__module__, t.__name__, v)
    sys.exit(msg)


def listglob(globs):
    l = []
    for x in globs:
        g = glob.glob(x)
        if len(g) == 0:
            sys.exit(u'pattern does not match any file: {}'.format(x))
        l += g
    return l


def try_makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            exception_exit(u'error creating directory: {}'.format(path))


def safe_regex(x, flags):
    try:
        return re.compile(x, flags)
    except:
        exception_exit(u'error parsing regex: {}'.format(x))


def try_search(r, w, i):
    if r is None:
        return None
    else:
        return r.search(w, i)


def is_exact(m, w):
    return m is not None and m.start() == 0 and m.end() == len(w)


def exact_match(r, w):
    m = r.match(w)
    return is_exact(m, w)


def try_exact_match(r, w):
    return r is not None and exact_match(r, w)


def try_capture(r, w):
    if r is None:
        return None
    m = r.match(w)
    if not is_exact(m, w):
        return None
    x = []
    if m.lastindex is not None:
        for i in xrange(m.lastindex):
            g = m.group(i + 1)
            if g is not None and g != u'':
                x.append(g)
    if len(x) == 0:
        x.append(m.group())
    return tuple(x)


def try_capture_join(r, w, sep=u' '):
    x = try_capture(r, w)
    if x is None:
        return None
    return sep.join(x)


class Counter(object):
    def __init__(self):
        self.distinct = set()
        self.total = 0

    def add(self, v):
        self.total += 1
        self.distinct.add(v)

    def types(self):
        return len(self.distinct)


#### Unit tests


class TestCapture(unittest.TestCase):
    def test_none(self):
        self.assertEqual(try_capture(None, u' abc'), None)

    def test_noparen(self):
        r = re.compile(ur'ab*c')
        self.assertEqual(try_capture(r, u' abc'), None)
        self.assertEqual(try_capture(r, u'abc '), None)
        self.assertEqual(try_capture(r, u'abc'), (u'abc',))
        self.assertEqual(try_capture(r, u'abbc'), (u'abbc',))

    def test_paren(self):
        r1 = re.compile(ur'a(b*)c')
        r2 = re.compile(ur'a(b+)?c')
        for r in r1, r2:
            self.assertEqual(try_capture(r, u' abc'), None)
            self.assertEqual(try_capture(r, u'abc '), None)
            self.assertEqual(try_capture(r, u'ac'), (u'ac',))
            self.assertEqual(try_capture(r, u'abc'), (u'b',))
            self.assertEqual(try_capture(r, u'abbc'), (u'bb',))

    def test_paren2(self):
        r1 = re.compile(ur'a(b+)?c(d+)?e')
        r2 = re.compile(ur'a(b*)c(d*)e')
        for r in r1, r2:
            self.assertEqual(try_capture(r, u' abcde'), None)
            self.assertEqual(try_capture(r, u'abcde '), None)
            self.assertEqual(try_capture(r, u'ace'), (u'ace',))
            self.assertEqual(try_capture(r, u'abce'), (u'b',))
            self.assertEqual(try_capture(r, u'acde'), (u'd',))
            self.assertEqual(try_capture(r, u'abcde'), (u'b', u'd'))
            self.assertEqual(try_capture(r, u'abbcdde'), (u'bb', u'dd'))


class TestCaptureJoin(unittest.TestCase):
    def test_noparen(self):
        r = re.compile(ur'ab*c')
        self.assertEqual(try_capture_join(r, u' abc'), None)
        self.assertEqual(try_capture_join(r, u'abc '), None)
        self.assertEqual(try_capture_join(r, u'abc'), u'abc')
        self.assertEqual(try_capture_join(r, u'abbc'), u'abbc')

    def test_paren(self):
        r1 = re.compile(ur'a(b*)c')
        r2 = re.compile(ur'a(b+)?c')
        for r in r1, r2:
            self.assertEqual(try_capture_join(r, u' abc'), None)
            self.assertEqual(try_capture_join(r, u'abc '), None)
            self.assertEqual(try_capture_join(r, u'ac'), u'ac')
            self.assertEqual(try_capture_join(r, u'abc'), u'b')
            self.assertEqual(try_capture_join(r, u'abbc'), u'bb')

    def test_paren2(self):
        r1 = re.compile(ur'a(b+)?c(d+)?e')
        r2 = re.compile(ur'a(b*)c(d*)e')
        for r in r1, r2:
            self.assertEqual(try_capture_join(r, u' abcde'), None)
            self.assertEqual(try_capture_join(r, u'abcde '), None)
            self.assertEqual(try_capture_join(r, u'ace'), u'ace')
            self.assertEqual(try_capture_join(r, u'abce'), u'b')
            self.assertEqual(try_capture_join(r, u'acde'), u'd')
            self.assertEqual(try_capture_join(r, u'abcde'), u'b d')
            self.assertEqual(try_capture_join(r, u'abbcdde'), u'bb dd')
            self.assertEqual(try_capture_join(r, u'abbcdde', u'x'), u'bbxdd')


if __name__ == u'__main__':
    unittest.main()
