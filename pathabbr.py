u"""Manipulating file name paths."""

import os.path
import unittest

def pathsplit(x):
    r = []
    cur = x
    while True:
        head, tail = os.path.split(cur)
        if head == cur and tail == u'':
            r.append(cur)
            break
        r.append(tail)
        if head == u'':
            break
        cur = head
    return tuple(reversed(r))


def pathnormalise(x):
    return os.path.join(*pathsplit(x))


def pathtail(x, n):
    if n == 0:
        return u''
    l = pathsplit(x)
    if len(l) > 0 and l[-1] == u'':
        n += 1
    if len(l) > n:
        l = l[-n:]
    return os.path.join(*l)


def _try_pathabbr(paths, n):
    reverse = {}
    result = {}
    for x in paths:
        normalised = pathnormalise(x)
        tail = pathtail(x, n)
        if tail in reverse and reverse[tail] != normalised:
            return None
        result[x] = tail
        reverse[tail] = normalised
    return result


def pathabbr(paths):
    n = 1
    while True:
        result = _try_pathabbr(paths, n)
        if result is not None:
            return result
        n += 1


#### Unit tests


class TestPathSplit(unittest.TestCase):
    def test_rel(self):
        self.assertEqual(pathsplit(u''), (u'',))
        self.assertEqual(pathsplit(u'a1'), (u'a1',))
        self.assertEqual(pathsplit(u'a1/a2'), (u'a1', u'a2'))
        self.assertEqual(pathsplit(u'a1/a2/a3'), (u'a1', u'a2', u'a3'))

    def test_abs(self):
        self.assertEqual(pathsplit(u'/'), (u'/',))
        self.assertEqual(pathsplit(u'/a1'), (u'/', u'a1'))
        self.assertEqual(pathsplit(u'/a1/a2'), (u'/', u'a1', u'a2'))
        self.assertEqual(pathsplit(u'/a1/a2/a3'), (u'/', u'a1', u'a2', u'a3'))

    def test_trail(self):
        self.assertEqual(pathsplit(u'/'), (u'/',))
        self.assertEqual(pathsplit(u'/a1/'), (u'/', u'a1', u''))
        self.assertEqual(pathsplit(u'/a1/a2/'), (u'/', u'a1', u'a2', u''))
        self.assertEqual(pathsplit(u'/a1/a2/a3/'), (u'/', u'a1', u'a2', u'a3', u''))

    def test_strange(self):
        self.assertEqual(pathsplit(u'a1////a2////a3'), (u'a1', u'a2', u'a3'))
        self.assertEqual(pathsplit(u'////a1////a2////a3'), (u'////', u'a1', u'a2', u'a3'))
        self.assertEqual(pathsplit(u'a1////a2////a3////'), (u'a1', u'a2', u'a3', u''))
        self.assertEqual(pathsplit(u'////a1////a2////a3////'), (u'////', u'a1', u'a2', u'a3', u''))


class TestPathNormalise(unittest.TestCase):
    def test_normal(self):
        for a in [
             u'',  u'a1',   u'a1/a2',   u'a1/a2/a3', 
            u'/', u'/a1',  u'/a1/a2',  u'/a1/a2/a3',
            u'/',  u'a1/',  u'a1/a2/',  u'a1/a2/a3/',
            u'/', u'/a1/', u'/a1/a2/', u'/a1/a2/a3/',
        ]:
            self.assertEqual(pathnormalise(a), a)

    def test_strange(self):
        self.assertEqual(pathnormalise(u'a1////a2////a3'), u'a1/a2/a3')
        self.assertEqual(pathnormalise(u'////a1////a2////a3'), u'////a1/a2/a3')
        self.assertEqual(pathnormalise(u'a1////a2////a3////'), u'a1/a2/a3/')
        self.assertEqual(pathnormalise(u'////a1////a2////a3////'), u'////a1/a2/a3/')


class TestPathTail(unittest.TestCase):
    def test_one(self):
        self.assertEqual(pathtail(u'a1', 0), u'')
        self.assertEqual(pathtail(u'a1', 1), u'a1')
        self.assertEqual(pathtail(u'a1', 2), u'a1')
        self.assertEqual(pathtail(u'a1', 3), u'a1')

    def test_rel(self):
        self.assertEqual(pathtail(u'a1/a2/a3', 0), u'')
        self.assertEqual(pathtail(u'a1/a2/a3', 1), u'a3')
        self.assertEqual(pathtail(u'a1/a2/a3', 2), u'a2/a3')
        self.assertEqual(pathtail(u'a1/a2/a3', 3), u'a1/a2/a3')
        self.assertEqual(pathtail(u'a1/a2/a3', 4), u'a1/a2/a3')
        self.assertEqual(pathtail(u'a1/a2/a3', 5), u'a1/a2/a3')

    def test_root(self):
        self.assertEqual(pathtail(u'/a1/a2/a3', 0), u'')
        self.assertEqual(pathtail(u'/a1/a2/a3', 1), u'a3')
        self.assertEqual(pathtail(u'/a1/a2/a3', 2), u'a2/a3')
        self.assertEqual(pathtail(u'/a1/a2/a3', 3), u'a1/a2/a3')
        self.assertEqual(pathtail(u'/a1/a2/a3', 4), u'/a1/a2/a3')
        self.assertEqual(pathtail(u'/a1/a2/a3', 5), u'/a1/a2/a3')

    def test_trail(self):
        self.assertEqual(pathtail(u'a3/', 0), u'')
        self.assertEqual(pathtail(u'a3/', 1), u'a3/')
        self.assertEqual(pathtail(u'a3/', 2), u'a3/')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 0), u'')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 1), u'a3/')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 2), u'a2/a3/')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 3), u'a1/a2/a3/')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 4), u'/a1/a2/a3/')
        self.assertEqual(pathtail(u'/a1/a2/a3/', 5), u'/a1/a2/a3/')

    def test_strange(self):
        self.assertEqual(pathtail(u'////a1////a2////a3////', 0), u'')
        self.assertEqual(pathtail(u'////a1////a2////a3////', 1), u'a3/')
        self.assertEqual(pathtail(u'////a1////a2////a3////', 2), u'a2/a3/')
        self.assertEqual(pathtail(u'////a1////a2////a3////', 3), u'a1/a2/a3/')
        self.assertEqual(pathtail(u'////a1////a2////a3////', 4), u'////a1/a2/a3/')
        self.assertEqual(pathtail(u'////a1////a2////a3////', 5), u'////a1/a2/a3/')


class TestTryPathAbbr(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 1), {
            u'a1/a2/a3': u'a3',
            u'b1/b2/b3': u'b3',
        })
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 2), {
            u'a1/a2/a3': u'a2/a3',
            u'b1/b2/b3': u'b2/b3',
        })
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 3), {
            u'a1/a2/a3': u'a1/a2/a3',
            u'b1/b2/b3': u'b1/b2/b3',
        })
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 4), {
            u'a1/a2/a3': u'a1/a2/a3',
            u'b1/b2/b3': u'b1/b2/b3',
        })

    def test_conflict(self):
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 0), None)
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3'], 1), {
            u'a1/a2/a3': u'a3',
            u'b1/b2/b3': u'b3',
        })
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/a3'], 1), None)
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/a3'], 2), {
            u'a1/a2/a3': u'a2/a3',
            u'b1/b2/a3': u'b2/a3',
        })
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/a2/a3'], 2), None)
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/a2/a3'], 3), {
            u'a1/a2/a3': u'a1/a2/a3',
            u'b1/a2/a3': u'b1/a2/a3',
        })

    def test_multi(self):
        # Multiple occurrences of the same path are fine
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3', u'b1/b2/b3'], 1), {
            u'a1/a2/a3': u'a3',
            u'b1/b2/b3': u'b3',
        })
        # Not a conflict: refers to the same path, can have the same abbreviation
        self.assertEqual(_try_pathabbr([u'a1/a2/a3', u'b1/b2/b3', u'b1/b2/b3', u'b1////b2////b3'], 1), {
            u'a1/a2/a3': u'a3',
            u'b1/b2/b3': u'b3',
            u'b1////b2////b3': u'b3',
        })
 

class TestPathAbbr(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pathabbr([u'a', u'b']), {
            u'a': u'a',
            u'b': u'b',
        })
        self.assertEqual(pathabbr([u'a1/a2', u'b1/b2']), {
            u'a1/a2': u'a2',
            u'b1/b2': u'b2',
        })
        self.assertEqual(pathabbr([u'a1/a2', u'b1/a2']), {
            u'a1/a2': u'a1/a2',
            u'b1/a2': u'b1/a2',
        })
        self.assertEqual(pathabbr([u'a1/a2/a3', u'b1/b2/a3']), {
            u'a1/a2/a3': u'a2/a3',
            u'b1/b2/a3': u'b2/a3',
        })
        self.assertEqual(pathabbr([u'a1/a2/a3', u'b1/a2/a3']), {
            u'a1/a2/a3': u'a1/a2/a3',
            u'b1/a2/a3': u'b1/a2/a3',
        })

    def test_lengths(self):
        self.assertEqual(pathabbr([u'a1/a2/a3', u'b1/b2/a3', u'c1']), {
            u'a1/a2/a3': u'a2/a3',
            u'b1/b2/a3': u'b2/a3',
            u'c1': u'c1',
        })

    def test_multi(self):
        # Multiple occurrences of the same path are fine
        self.assertEqual(pathabbr([u'a', u'b', u'b']), {
            u'a': u'a',
            u'b': u'b',
        })
        # Not a conflict: refers to the same path, can have the same abbreviation
        self.assertEqual(pathabbr([u'a1/a2', u'b1/b2', u'b1////b2']), {
            u'a1/a2': u'a2',
            u'b1/b2': u'b2',
            u'b1////b2': u'b2',
        })


if __name__ == u'__main__':
    unittest.main()
