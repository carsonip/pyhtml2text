import pytest
from pyhtml2text import html2text


def test_simple_html():
    html = '<body>foo</body>'
    assert html2text(html) == 'foo\n'


def test_large_html():
    html = '<body><div>%s</div></body>' % ('a' * 100000)
    assert html2text(html) == ('a' * 100000) + '\n'


def test_br_in_div():
    # There should be only 2 \n instead of 3 unless there is something after <br>
    html = '<body>foo<div><br></div>bar</body>'
    assert html2text(html) == 'foo\n\nbar\n'

    html = '<body>foo<div><br>bar</div>baz</body>'
    assert html2text(html) == 'foo\n\nbar\nbaz\n'
