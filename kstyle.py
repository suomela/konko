u"""How to format Konko output."""

excel_format = {
    u"bold":  {u'bold': True},
    u"hl":    {u'bold': True, u'font_color': u'#dd0000'},
    u"key":   {u'align': u'center'},
    u"right": {u'align': u'right'},
    u"light": {u'font_color': u'#999999'},
}

# .c: compound
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
    border: 1px dotted #000;
    font-size: 1.5em;
    background-color: #eee;
}
.c:hover {
    color: #fff;
    background-color: #000;
}

"""
