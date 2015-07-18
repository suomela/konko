import unittest
import filtering


def number_printable(s, i):
    return '{} ({})'.format(s, i)


def number_safe(s, i):
    return '{}-{}'.format(s, i)


class UniqueNames:
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
            if val != '' and val not in self.used:
                self.used.add(val)
                self.keymap[key] = val
                return val
            i = 1 if i is None else i + 1



#### Unit tests


class TestUniqueNames(unittest.TestCase):
    def test_printable(self):
        u = UniqueNames(filtering.printable, number_printable)
        for i in range(3):
            self.assertEqual(u.get('abc'), 'abc')
            self.assertEqual(u.get('123\n456'), '123 456')
            self.assertEqual(u.get('abc\b'), 'abc (1)')
            self.assertEqual(u.get('a\bbc'), 'abc (2)')
            self.assertEqual(u.get('abc\n'), 'abc ')
            self.assertEqual(u.get('abc\r'), 'abc  (1)')
            self.assertEqual(u.get('abc\t'), 'abc  (2)')
            self.assertEqual(u.get('äbc'), 'äbc')
            self.assertEqual(u.get('123 456'), '123 456 (1)')
            self.assertEqual(u.get('123\t456'), '123 456 (2)')
            self.assertEqual(u.get(''), ' (1)')
            self.assertEqual(u.get('\b'), ' (2)')
            self.assertEqual(u.get('\0'), ' (3)')

    def test_safe(self):
        u = UniqueNames(filtering.safe, number_safe)
        for i in range(3):
            self.assertEqual(u.get('abc'), 'abc')
            self.assertEqual(u.get('123\n456'), '123-456')
            self.assertEqual(u.get('abc\b'), 'abc-1')
            self.assertEqual(u.get('a\bbc'), 'a-bc')
            self.assertEqual(u.get('abc\n'), 'abc-2')
            self.assertEqual(u.get('abc\r'), 'abc-3')
            self.assertEqual(u.get('abc\t'), 'abc-4')
            self.assertEqual(u.get('äbc'), 'abc-5')
            self.assertEqual(u.get('123 456'), '123-456-1')
            self.assertEqual(u.get('123\t456'), '123-456-2')
            self.assertEqual(u.get(''), '-')
            self.assertEqual(u.get('\b'), '--1')
            self.assertEqual(u.get('\0'), '--2')


if __name__ == '__main__':
    unittest.main()
