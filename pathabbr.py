"""Manipulating file name paths."""

import os.path
import unittest

def pathsplit(x):
    r = []
    cur = x
    while True:
        head, tail = os.path.split(cur)
        if head == cur and tail == '':
            r.append(cur)
            break
        r.append(tail)
        if head == '':
            break
        cur = head
    return tuple(reversed(r))


def pathnormalise(x):
    return os.path.join(*pathsplit(x))


def pathtail(x, n):
    if n == 0:
        return ''
    l = pathsplit(x)
    if len(l) > 0 and l[-1] == '':
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
        self.assertEqual(pathsplit(''), ('',))
        self.assertEqual(pathsplit('a1'), ('a1',))
        self.assertEqual(pathsplit('a1/a2'), ('a1', 'a2'))
        self.assertEqual(pathsplit('a1/a2/a3'), ('a1', 'a2', 'a3'))

    def test_abs(self):
        self.assertEqual(pathsplit('/'), ('/',))
        self.assertEqual(pathsplit('/a1'), ('/', 'a1'))
        self.assertEqual(pathsplit('/a1/a2'), ('/', 'a1', 'a2'))
        self.assertEqual(pathsplit('/a1/a2/a3'), ('/', 'a1', 'a2', 'a3'))

    def test_trail(self):
        self.assertEqual(pathsplit('/'), ('/',))
        self.assertEqual(pathsplit('/a1/'), ('/', 'a1', ''))
        self.assertEqual(pathsplit('/a1/a2/'), ('/', 'a1', 'a2', ''))
        self.assertEqual(pathsplit('/a1/a2/a3/'), ('/', 'a1', 'a2', 'a3', ''))

    def test_strange(self):
        self.assertEqual(pathsplit('a1////a2////a3'), ('a1', 'a2', 'a3'))
        self.assertEqual(pathsplit('////a1////a2////a3'), ('////', 'a1', 'a2', 'a3'))
        self.assertEqual(pathsplit('a1////a2////a3////'), ('a1', 'a2', 'a3', ''))
        self.assertEqual(pathsplit('////a1////a2////a3////'), ('////', 'a1', 'a2', 'a3', ''))


class TestPathNormalise(unittest.TestCase):
    def test_normal(self):
        for a in [
             '',  'a1',   'a1/a2',   'a1/a2/a3', 
            '/', '/a1',  '/a1/a2',  '/a1/a2/a3',
            '/',  'a1/',  'a1/a2/',  'a1/a2/a3/',
            '/', '/a1/', '/a1/a2/', '/a1/a2/a3/',
        ]:
            self.assertEqual(pathnormalise(a), a)

    def test_strange(self):
        self.assertEqual(pathnormalise('a1////a2////a3'), 'a1/a2/a3')
        self.assertEqual(pathnormalise('////a1////a2////a3'), '////a1/a2/a3')
        self.assertEqual(pathnormalise('a1////a2////a3////'), 'a1/a2/a3/')
        self.assertEqual(pathnormalise('////a1////a2////a3////'), '////a1/a2/a3/')


class TestPathTail(unittest.TestCase):
    def test_one(self):
        self.assertEqual(pathtail('a1', 0), '')
        self.assertEqual(pathtail('a1', 1), 'a1')
        self.assertEqual(pathtail('a1', 2), 'a1')
        self.assertEqual(pathtail('a1', 3), 'a1')

    def test_rel(self):
        self.assertEqual(pathtail('a1/a2/a3', 0), '')
        self.assertEqual(pathtail('a1/a2/a3', 1), 'a3')
        self.assertEqual(pathtail('a1/a2/a3', 2), 'a2/a3')
        self.assertEqual(pathtail('a1/a2/a3', 3), 'a1/a2/a3')
        self.assertEqual(pathtail('a1/a2/a3', 4), 'a1/a2/a3')
        self.assertEqual(pathtail('a1/a2/a3', 5), 'a1/a2/a3')

    def test_root(self):
        self.assertEqual(pathtail('/a1/a2/a3', 0), '')
        self.assertEqual(pathtail('/a1/a2/a3', 1), 'a3')
        self.assertEqual(pathtail('/a1/a2/a3', 2), 'a2/a3')
        self.assertEqual(pathtail('/a1/a2/a3', 3), 'a1/a2/a3')
        self.assertEqual(pathtail('/a1/a2/a3', 4), '/a1/a2/a3')
        self.assertEqual(pathtail('/a1/a2/a3', 5), '/a1/a2/a3')

    def test_trail(self):
        self.assertEqual(pathtail('a3/', 0), '')
        self.assertEqual(pathtail('a3/', 1), 'a3/')
        self.assertEqual(pathtail('a3/', 2), 'a3/')
        self.assertEqual(pathtail('/a1/a2/a3/', 0), '')
        self.assertEqual(pathtail('/a1/a2/a3/', 1), 'a3/')
        self.assertEqual(pathtail('/a1/a2/a3/', 2), 'a2/a3/')
        self.assertEqual(pathtail('/a1/a2/a3/', 3), 'a1/a2/a3/')
        self.assertEqual(pathtail('/a1/a2/a3/', 4), '/a1/a2/a3/')
        self.assertEqual(pathtail('/a1/a2/a3/', 5), '/a1/a2/a3/')

    def test_strange(self):
        self.assertEqual(pathtail('////a1////a2////a3////', 0), '')
        self.assertEqual(pathtail('////a1////a2////a3////', 1), 'a3/')
        self.assertEqual(pathtail('////a1////a2////a3////', 2), 'a2/a3/')
        self.assertEqual(pathtail('////a1////a2////a3////', 3), 'a1/a2/a3/')
        self.assertEqual(pathtail('////a1////a2////a3////', 4), '////a1/a2/a3/')
        self.assertEqual(pathtail('////a1////a2////a3////', 5), '////a1/a2/a3/')


class TestTryPathAbbr(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 1), {
            'a1/a2/a3': 'a3',
            'b1/b2/b3': 'b3',
        })
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 2), {
            'a1/a2/a3': 'a2/a3',
            'b1/b2/b3': 'b2/b3',
        })
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 3), {
            'a1/a2/a3': 'a1/a2/a3',
            'b1/b2/b3': 'b1/b2/b3',
        })
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 4), {
            'a1/a2/a3': 'a1/a2/a3',
            'b1/b2/b3': 'b1/b2/b3',
        })

    def test_conflict(self):
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 0), None)
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3'], 1), {
            'a1/a2/a3': 'a3',
            'b1/b2/b3': 'b3',
        })
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/a3'], 1), None)
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/a3'], 2), {
            'a1/a2/a3': 'a2/a3',
            'b1/b2/a3': 'b2/a3',
        })
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/a2/a3'], 2), None)
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/a2/a3'], 3), {
            'a1/a2/a3': 'a1/a2/a3',
            'b1/a2/a3': 'b1/a2/a3',
        })

    def test_multi(self):
        # Multiple occurrences of the same path are fine
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3', 'b1/b2/b3'], 1), {
            'a1/a2/a3': 'a3',
            'b1/b2/b3': 'b3',
        })
        # Not a conflict: refers to the same path, can have the same abbreviation
        self.assertEqual(_try_pathabbr(['a1/a2/a3', 'b1/b2/b3', 'b1/b2/b3', 'b1////b2////b3'], 1), {
            'a1/a2/a3': 'a3',
            'b1/b2/b3': 'b3',
            'b1////b2////b3': 'b3',
        })
 

class TestPathAbbr(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pathabbr(['a', 'b']), {
            'a': 'a',
            'b': 'b',
        })
        self.assertEqual(pathabbr(['a1/a2', 'b1/b2']), {
            'a1/a2': 'a2',
            'b1/b2': 'b2',
        })
        self.assertEqual(pathabbr(['a1/a2', 'b1/a2']), {
            'a1/a2': 'a1/a2',
            'b1/a2': 'b1/a2',
        })
        self.assertEqual(pathabbr(['a1/a2/a3', 'b1/b2/a3']), {
            'a1/a2/a3': 'a2/a3',
            'b1/b2/a3': 'b2/a3',
        })
        self.assertEqual(pathabbr(['a1/a2/a3', 'b1/a2/a3']), {
            'a1/a2/a3': 'a1/a2/a3',
            'b1/a2/a3': 'b1/a2/a3',
        })

    def test_lengths(self):
        self.assertEqual(pathabbr(['a1/a2/a3', 'b1/b2/a3', 'c1']), {
            'a1/a2/a3': 'a2/a3',
            'b1/b2/a3': 'b2/a3',
            'c1': 'c1',
        })

    def test_multi(self):
        # Multiple occurrences of the same path are fine
        self.assertEqual(pathabbr(['a', 'b', 'b']), {
            'a': 'a',
            'b': 'b',
        })
        # Not a conflict: refers to the same path, can have the same abbreviation
        self.assertEqual(pathabbr(['a1/a2', 'b1/b2', 'b1////b2']), {
            'a1/a2': 'a2',
            'b1/b2': 'b2',
            'b1////b2': 'b2',
        })


if __name__ == '__main__':
    unittest.main()
