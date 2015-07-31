u"""How to format Konko output."""

excel_format = {
    u"bold":  {u'bold': True},
    u"hl":    {u'bold': True, u'font_color': u'#dd0000'},
    u"key":   {u'align': u'center', u'bold': True},
    u"right": {u'align': u'right'},
    u"light": {u'font_color': u'#999999'},
}


css = u"""
.sep, .tag, .del {
    color: #999;
}
.tag, .del {
    font-size: 0.8em;
}
.sample {
    color: #00f;
    font-weight: 700;
}
.match {
    color: #d00;
    font-weight: 700;
}
:target {
    color: #0a0;
    font-size: 1.5em;
}
.word:hover {
    color: #fff;
    background-color: #000;
}
.tag:hover {
    color: #fff;
    background-color: #00c;
}
.sep:hover {
    color: #fff;
    background-color: #c00;
}

"""
