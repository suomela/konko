u"""Reading Konko configuration file."""

from __future__ import with_statement
from __future__ import absolute_import
import json
import re
import sys
import kutil
from io import open


class KConfig(object):
    def __init__(self, file):
        self.file = file
        self.search_flags = 0
        self.tag_flags = 0
        self.word_flags = 0
        self.source = []
        self.skip_files = []
        self.search = []
        self.delete = []
        self.delete_pair = []
        self.text = None
        self.sample = None
        self.tag = None
        self.word = re.compile(ur"\w+([-']\w+)*")
        self.output_dir = u'output'
        self.encoding = u'ascii'
        self.context = 100
        self.server_port = 8000
        with open(file) as f:
            cfg = json.load(f)
            self.set_config([], cfg)        

    def error(self, path, msg):
        if len(path) == 0:
            elem = u'root element'
        else:
            elem = u'element {}'.format(u'.'.join([unicode(x) for x in path]))
        sys.exit(u'{}: {}: {}'.format(
            self.file, elem, msg
        ))

    def type_error(self, path, exp, got):
        self.error(path, u'expected {}, got {}'.format(
            exp.__name__, type(got).__name__
        ))

    def key_error(self, path, key):
        self.error(path, u'unsupported key "{}"'.format(key))

    def get(self, path):
        p = []
        c = self.config
        for e in path:
            if not isinstance(c, dict):
                self.type_error(p, dict, c)
            if e not in c:
                return None
            c = c[e]
        return c

    def boolean(self, path, default):
        v = self.get(path)
        if v is None:
            return default
        elif isinstance(v, bool):
            return v
        else:
            self.type_error(path, bool, v)

    def expect(self, path, exp, got):
        if not isinstance(got, exp):
            self.type_error(path, exp, got)

    def expect_string_list(self, path, got):
        self.expect(path, list, got)
        for i, v in enumerate(got):
            p = path + [i]
            self.expect(p, unicode, v)

    def set_config(self, path0, val0):
        self.expect(path0, dict, val0)
        for key, v in val0.items():
            p = path0 + [key]
            if key == u'search-ignore-case':
                self.expect(p, bool, v)
                self.search_flags = re.IGNORECASE if v else 0
            elif key == u'tag-ignore-case':
                self.expect(p, bool, v)
                self.tag_flags = re.IGNORECASE if v else 0
            elif key == u'word-ignore-case':
                self.expect(p, bool, v)
                self.word_flags = re.IGNORECASE if v else 0
        for key, v in val0.items():
            p = path0 + [key]
            if key in (u'search-ignore-case', u'tag-ignore-case', u'word-ignore-case'):
                pass
            elif key == u'source':
                self.set_source(p, v)
            elif key == u'output-dir':
                self.expect(p, unicode, v)
                self.output_dir = v
            elif key == u'encoding':
                self.expect(p, unicode, v)
                self.encoding = v
            elif key == u'context':
                self.expect(p, int, v)
                self.context = v
            elif key == u'server-port':
                self.expect(p, int, v)
                self.server_port = v
            elif key == u'search':
                self.set_search(p, v)
            elif key == u'skip-files':
                self.expect_string_list(p, v)
                self.skip_files += v
            elif key == u'delete':
                self.set_delete(p, v)
            elif key == u'text':
                self.expect(p, unicode, v)
                self.text = kutil.safe_regex(v, self.tag_flags)
            elif key == u'sample':
                self.expect(p, unicode, v)
                self.sample = kutil.safe_regex(v, self.tag_flags)
            elif key == u'tag':
                self.expect(p, unicode, v)
                self.tag = kutil.safe_regex(v, self.tag_flags)
            elif key == u'word':
                self.expect(p, unicode, v)
                self.word = kutil.safe_regex(v, self.word_flags)
            else:
                self.key_error(path0, key)

    def set_source(self, path, v):
        self.expect(path, dict, v)
        for key, val in sorted(v.items()):
            p = path + [key]
            self.expect_string_list(p, val)
            self.source.append((key, val))

    def set_search(self, path, v):
        self.expect(path, dict, v)
        for key, val in sorted(v.items()):
            p = path + [key]
            self.expect(p, unicode, val)
            re = kutil.safe_regex(val, self.search_flags)
            self.search.append((key, re))

    def set_delete(self, path, v):
        self.expect(path, list, v)
        for i, x in enumerate(v):
            p = path + [i]
            self.set_delete_one(p, x)

    def set_delete_one(self, path, v):
        self.expect_string_list(path, v)
        l = [kutil.safe_regex(x, self.tag_flags) for x in v]
        if len(l) == 1:
            self.delete.append(l[0])
        elif len(l) == 2:
            self.delete_pair.append(l)
        else:
            self.error(path, u'expected 1 or 2 elements')
