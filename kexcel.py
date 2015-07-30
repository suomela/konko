u"""Generating Excel files."""

from __future__ import absolute_import
import collections
import xlsxwriter
import kstyle
import kutil


class Excel(object):
    def __init__(self, filename):
        try:
            self.wb = xlsxwriter.Workbook(filename)
        except:
            kutil.exception_exit(u'error creating output file: {}'.format(filename))
        self.fmt = dict(( k, self.wb.add_format(v)) for k, v in kstyle.excel_format.items())
        self.sheets = []

    def sheet(self, name, cols):
        return Sheet(self, name, cols)

    def close(self):
        for s in self.sheets:
            s.close()
        self.wb.close()


class Sheet(object):
    def __init__(self, xl, name, cols):
        self.isopen = True
        self.xl = xl
        self.ws = self.xl.wb.add_worksheet(name)
        self.cols = cols
        self.widths = collections.defaultdict(int)
        self.r = 1
        self.c = 0
        self.xl.sheets.append(self)

    def close(self):
        if not self.isopen:
            return
        self.ws.set_row(0, None, self.xl.fmt[u"bold"])
        self.r = 0
        self.c = 0
        for col in self.cols:
            name = col[0]
            self.write_string(name)
        for c, col in enumerate(self.cols):
            fmt = col[1] if len(col) > 1 else None
            width = col[2] if len(col) > 2 else None
            if width is None:
                width = self._autoscale(c)
            if fmt is None:
                self.ws.set_column(c, c, width)
            else:
                self.ws.set_column(c, c, width, self.xl.fmt[fmt])
        self.ws.freeze_panes(1, 0)
        self.isopen = False

    def next_row(self):
        self.r += 1
        self.c = 0

    def write_number(self, v):
        if v is not None:
            self.ws.write_number(self.r, self.c, v)
            self._tell(len(unicode(v)))
        self.c += 1

    def write_string(self, v):
        if v is not None:
            self.ws.write_string(self.r, self.c, v)
            self._tell(len(v))
        self.c += 1

    def write_url(self, url, v):
        if v is not None:
            self.ws.write_url(self.r, self.c, url, None, v)
            self._tell(len(v))
        self.c += 1

    def write_rich(self, v):
        l = []
        s = u""
        for fmt, txt in v:
            if fmt != u"normal":
                l.append(self.xl.fmt[fmt])
            l.append(txt)
            s += txt
        if len(l) > 0:
            self.ws.write_rich_string(self.r, self.c, *l)
        self._tell(len(s))
        self.c += 1

    def _autoscale(self, c):
        t = 10
        k = 0.8
        w = self.widths[c] + 1
        if w > t:
            w = t + int(k * (w - t))
        return w

    def _tell(self, w):
        self.widths[self.c] = max(self.widths[self.c], w)

