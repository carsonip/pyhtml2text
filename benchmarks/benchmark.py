import timeit
from tabulate import tabulate


# https://stackoverflow.com/a/1094933/3315725
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


NUMBER = 10
SIZE_LIST = [10, 1024, 2048]

timers = {
    'pyhtml2text': timeit.Timer('html2text(html)',
                                setup='from pyhtml2text import html2text; from __main__ import html'),
    'html2text': timeit.Timer('h.handle(html)',
                              setup='import html2text as python_html2text; h = python_html2text.HTML2Text();  from __main__ import html')
}

rows = []

for k, v in timers.items():
    results = []
    for s in SIZE_LIST:
        html = b'<div>' + (b'a' * s) + b'</div>'
        results.append(v.timeit(NUMBER))
    rows.append([k] + results)

print(tabulate(rows, headers=[''] + [sizeof_fmt(s) for s in SIZE_LIST]))
