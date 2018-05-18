import pytest
from pyhtml2text import html2text


def test_simple_html():
    html = b'<body>foo</body>'
    assert html2text(html) == b'foo\n'


def test_large_html():
    html = b'<body><div>' + (b'a' * 100000) + b'</div></body>'
    assert html2text(html) == (b'a' * 100000) + b'\n'


def test_br_in_div():
    # There should be only 2 \n instead of 3 unless there is something after <br>
    html = b'<body>foo<div><br></div>bar</body>'
    assert html2text(html) == b'foo\n\nbar\n'

    html = b'<body>foo<div><br>bar</div>baz</body>'
    assert html2text(html) == b'foo\n\nbar\nbaz\n'
