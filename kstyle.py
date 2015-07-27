"""How to format Konko output."""

excel_format = {
    "bold":  {'bold': True},
    "hl":    {'bold': True, 'font_color': '#dd0000'},
    "key":   {'align': 'center', 'bold': True},
    "right": {'align': 'right'},
    "light": {'font_color': '#999999'},
}


css = """
.sep, .tag, .del {
    color: #999;
}
.tag, .del {
    font-size: 0.8em;
}
.show {
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
"""
