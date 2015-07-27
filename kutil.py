"""Miscellaneous utility functions."""

import unittest
import glob
import re
import sys


def exception_exit(msg):
    t, v, tb = sys.exc_info()
    print('{}.{}: {}'.format(t.__module__, t.__name__, v), file=sys.stderr)
    sys.exit(msg)


def listglob(globs):
    l = []
    for x in globs:
        g = glob.glob(x)
        if len(g) == 0:
            sys.exit('pattern does not match any file: {}'.format(x))
        l += g
    return l


def safe_regex(x, flags):
    try:
        return re.compile(x, flags)
    except:
        exception_exit('error parsing regex: {}'.format(x))


def try_search(re, w, i):
    if re is None:
        return None
    else:
        return re.search(w, i)


def is_exact(m, w):
    return m is not None and m.start() == 0 and m.end() == len(w)


def exact_match(re, w):
    m = re.match(w)
    return is_exact(m, w)


def try_exact_match(re, w):
    return re is not None and exact_match(re, w)


def try_capture(re, w):
    m = re.match(w)
    if not is_exact(m, w):
        return None
    r = []
    if m.lastindex is not None:
        for i in range(m.lastindex):
            g = m.group(i + 1)
            if g is not None and g != '':
                r.append(g)
    if len(r) == 0:
        r.append(m.group())
    return tuple(r)


def try_capture_join(re, w, sep=' '):
    r = try_capture(re, w)
    if r is None:
        return None
    return sep.join(r)


class Counter:
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
    def test_noparen(self):
        r = re.compile(r'ab*c')
        self.assertEqual(try_capture(r, ' abc'), None)
        self.assertEqual(try_capture(r, 'abc '), None)
        self.assertEqual(try_capture(r, 'abc'), ('abc',))
        self.assertEqual(try_capture(r, 'abbc'), ('abbc',))

    def test_paren(self):
        r1 = re.compile(r'a(b*)c')
        r2 = re.compile(r'a(b+)?c')
        for r in r1, r2:
            self.assertEqual(try_capture(r, ' abc'), None)
            self.assertEqual(try_capture(r, 'abc '), None)
            self.assertEqual(try_capture(r, 'ac'), ('ac',))
            self.assertEqual(try_capture(r, 'abc'), ('b',))
            self.assertEqual(try_capture(r, 'abbc'), ('bb',))

    def test_paren2(self):
        r1 = re.compile(r'a(b+)?c(d+)?e')
        r2 = re.compile(r'a(b*)c(d*)e')
        for r in r1, r2:
            self.assertEqual(try_capture(r, ' abcde'), None)
            self.assertEqual(try_capture(r, 'abcde '), None)
            self.assertEqual(try_capture(r, 'ace'), ('ace',))
            self.assertEqual(try_capture(r, 'abce'), ('b',))
            self.assertEqual(try_capture(r, 'acde'), ('d',))
            self.assertEqual(try_capture(r, 'abcde'), ('b', 'd'))
            self.assertEqual(try_capture(r, 'abbcdde'), ('bb', 'dd'))


class TestCaptureJoin(unittest.TestCase):
    def test_noparen(self):
        r = re.compile(r'ab*c')
        self.assertEqual(try_capture_join(r, ' abc'), None)
        self.assertEqual(try_capture_join(r, 'abc '), None)
        self.assertEqual(try_capture_join(r, 'abc'), 'abc')
        self.assertEqual(try_capture_join(r, 'abbc'), 'abbc')

    def test_paren(self):
        r1 = re.compile(r'a(b*)c')
        r2 = re.compile(r'a(b+)?c')
        for r in r1, r2:
            self.assertEqual(try_capture_join(r, ' abc'), None)
            self.assertEqual(try_capture_join(r, 'abc '), None)
            self.assertEqual(try_capture_join(r, 'ac'), 'ac')
            self.assertEqual(try_capture_join(r, 'abc'), 'b')
            self.assertEqual(try_capture_join(r, 'abbc'), 'bb')

    def test_paren2(self):
        r1 = re.compile(r'a(b+)?c(d+)?e')
        r2 = re.compile(r'a(b*)c(d*)e')
        for r in r1, r2:
            self.assertEqual(try_capture_join(r, ' abcde'), None)
            self.assertEqual(try_capture_join(r, 'abcde '), None)
            self.assertEqual(try_capture_join(r, 'ace'), 'ace')
            self.assertEqual(try_capture_join(r, 'abce'), 'b')
            self.assertEqual(try_capture_join(r, 'acde'), 'd')
            self.assertEqual(try_capture_join(r, 'abcde'), 'b d')
            self.assertEqual(try_capture_join(r, 'abbcdde'), 'bb dd')
            self.assertEqual(try_capture_join(r, 'abbcdde', 'x'), 'bbxdd')


if __name__ == '__main__':
    unittest.main()
