import timeit
import signal
from tabulate import tabulate


# https://stackoverflow.com/a/1094933/3315725
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class Timeout(Exception):
    pass


def timeout_handler(signum, frame):
    raise Timeout()


signal.signal(signal.SIGALRM, timeout_handler)

NUMBER = 10
REPEAT_COUNT = 3
TIMEOUT = 10
SIZE_LIST = [10, 1024, 2 * 1024, 100 * 1024, 1024 * 1024]

timers = {
    'pyhtml2text': timeit.Timer('html2text(html)',
                                setup='from pyhtml2text import html2text; from __main__ import html'),
    'html2text': timeit.Timer('h.handle(html)',
                              setup='import html2text as python_html2text; h = python_html2text.HTML2Text();  from __main__ import html'),
    'bs4+html.parser': timeit.Timer('BeautifulSoup(html, "html.parser").get_text()',
                                    setup='from bs4 import BeautifulSoup; from __main__ import html'),
    'bs4+lxml': timeit.Timer('BeautifulSoup(html, "lxml").get_text()',
                             setup='from bs4 import BeautifulSoup; from __main__ import html'),
}

rows = []

for k, v in timers.items():
    results = []
    for s in SIZE_LIST:
        html = b'<div>' + (b'a' * s) + b'</div>'
        signal.alarm(TIMEOUT)
        try:
            t = min(v.repeat(repeat=REPEAT_COUNT, number=NUMBER))
        except Timeout:
            results.append('>%s' % TIMEOUT)
        else:
            signal.alarm(0)  # Cancel alarm
            results.append(t)

    rows.append([k] + results)

print('Runtime (in seconds) of processing %s times of various input sizes, best of %s: ' % (NUMBER, REPEAT_COUNT))
print(tabulate(rows, headers=[''] + [sizeof_fmt(s) for s in SIZE_LIST]))
