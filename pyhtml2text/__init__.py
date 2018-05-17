# -*- coding: utf-8 -*-
import cffi
import os

ffi = cffi.FFI()
ffi.cdef('char *cffi_html2text(char *html);'
         'void cffi_free(char *ret);')
here = os.path.abspath(os.path.dirname(__file__))
C = ffi.dlopen(os.path.join(here, 'libhtml2text.so'))

__all__ = ['html2text']


def html2text(html):
    if isinstance(html, unicode):
        html = html.encode('utf-8')
    x = C.cffi_html2text(html)

    if x == ffi.NULL:
        raise Exception('NULL')
    s = bytes(ffi.string(x))
    C.cffi_free(x)
    return s
