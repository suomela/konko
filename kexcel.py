"""Generating Excel files."""

import collections
import xlsxwriter
import kstyle
import kutil


class Excel:
    def __init__(self, filename, cols):
        try:
            self.wb = xlsxwriter.Workbook(filename)
        except:
            kutil.exception_exit('error creating output file: {}'.format(filename))
        self.cols = cols
        self.fmt = { k: self.wb.add_format(v) for k, v in kstyle.excel_format.items() }
        self.ws = self.wb.add_worksheet()
        self.widths = collections.defaultdict(int)
        self.r = 1
        self.c = 0

    def close(self):
        self.ws.set_row(0, None, self.fmt["bold"])
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
                self.ws.set_column(c, c, width, self.fmt[fmt])
        self.ws.freeze_panes(1, 0)
        self.wb.close()

    def next_row(self):
        self.r += 1
        self.c = 0

    def write_number(self, v):
        if v is not None:
            self.ws.write_number(self.r, self.c, v)
            self._tell(len(str(v)))
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
        s = ""
        for fmt, txt in v:
            if fmt != "normal":
                l.append(self.fmt[fmt])
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

