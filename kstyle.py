u"""How to format Konko output."""

excel_format = {
    u"bold":  {u'bold': True},
    u"hl":    {u'bold': True, u'font_color': u'#dd0000'},
    u"key":   {u'align': u'center', u'bold': True},
    u"right": {u'align': u'right'},
    u"light": {u'font_color': u'#999999'},
}

# .s: separator
# .t: tag
# .w: word
# .d: deleted
# .i: sample identifier
# .m: matching word
css = u"""
.s, .t, .d {
    color: #999;
}
.t, .d {
    font-size: 0.8em;
}
.i {
    color: #00f;
    font-weight: 700;
}
.m {
    color: #d00;
    font-weight: 700;
}
:target {
    color: #0a0;
    font-size: 1.5em;
}
.w:hover {
    color: #fff;
    background-color: #000;
}
.t:hover {
    color: #fff;
    background-color: #00c;
}
.s:hover {
    color: #fff;
    background-color: #c00;
}

"""
