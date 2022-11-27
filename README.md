[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-dict.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-dict/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_dict)](https://pypi.org/project/gqylpy_dict)
[![License](https://img.shields.io/pypi/l/gqylpy_dict)](https://github.com/gqylpy/gqylpy-dict/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_dict/month)](https://pepy.tech/project/gqylpy_dict)

# gqylpy-dict

> `gqylpy-dict` 基于内置 `dict`，它是对内置 `dict` 的增强。`dict` 能做的它能做，`dict` 不能做的它更能做。

<kbd>pip3 install gqylpy_dict</kbd>

```python
>>> from gqylpy_dict import gdict

>>> gdict == dict
True

>>> gdict is dict
False

>>> x = {'a': [{'b': 'B'}]}
>>> x = gdict(x)
>>> x.a[0].b
'B'

>>> x.deepget('a[0].b')
'B'
```
