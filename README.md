# pyhtml2text: Python wrapper for html2text

[![Build Status](https://travis-ci.org/carsonip/pyhtml2text.svg?branch=master)](https://travis-ci.org/carsonip/pyhtml2text)

This is a Python wrapper of the C++ [html2text](http://www.mbayer.de/html2text/) tool. The original C++ html2text project is slightly modified such that Python can use the functions through [cffi](https://cffi.readthedocs.io). 

html2text was written up to version 1.2.2 by Arno Unkrig for GMRS, up to version 1.3.2 by Martin Bayer. An active fork is currently maintained by Debian [here](https://anonscm.debian.org/cgit/collab-maint/html2text.git/).

The html2text C++ code is licensed in GPLv2. Therefore this wrapper will also be licensed in GPLv2.

## Installation

```bash
pip install git+https://github.com/carsonip/pyhtml2text.git
```

## Example

```python
>>> from pyhtml2text import html2text
>>> html2text('<div>hello world</div>')
'hello world\n'
>>> html2text('<ol><li>one</li><li>two</li><li>three</li></ol>')
'   1. one\n   2. two\n   3. three\n'
```

## Development

1. In the project directory, `cd` into the C++ project then compile the html2text as a shared library.
     ```bash
    cd c/html2text
    ./configure
    make
    ```

2. Under `c/html2text`, there should be a `libhtml2text.so` now. Place it next to the Python code.
    ```bash
    cp libhtml2text.so ../../pyhtml2text
    ```
    
3. The cffi function in Python code should be able to load the `.so` now.
