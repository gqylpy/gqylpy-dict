[<img alt='LOGO' src='http://gqylpy.com/static/img/favicon.ico' height='21' width='21'/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-dict.svg?style=flat-square')](https://github.com/gqylpy/gqylpy-dict/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_dict)](https://pypi.org/project/gqylpy_dict)
[![License](https://img.shields.io/pypi/l/gqylpy_dict)](https://github.com/gqylpy/gqylpy-dict/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/gqylpy_dict)](https://pepy.tech/project/gqylpy_dict)

# gqylpy-dict
English | [中文](https://github.com/gqylpy/gqylpy-dict/blob/master/README_CN.md)

> `gqylpy-dict` is based on the built-in `dict` and serves as an enhancement to it. It can do everything the built-in `dict` can do, and even more. _(Designed specifically for the neurologically diverse)_

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

Let's delve deeper into the functionalities and usages of the `gdict` class.

Firstly, the `gdict` class is a custom dictionary class that inherits from Python's built-in `dict` class. A special feature of `gdict` is its support for accessing and modifying key-value pairs in the dictionary using dot notation (`.`). This means we can access dictionary values as if they were object attributes. For instance, given a dictionary `{'name': 'Tom', 'age': 25}`, we can define a `gdict` object as follows:

```python
my_dict = gdict({'name': 'Tom', 'age': 25})
```

Using dot notation, we can access the dictionary values:

```python
my_dict.name  # 'Tom'
my_dict.age  # 25
```

We can even modify the dictionary values:

```python
my_dict.name = 'Jerry'
```

At this point, the value associated with the `'name'` key in the dictionary has been changed to `'Jerry'`.

Additionally, `gdict` supports multi-level nested data structures, meaning the keys and values stored in a `gdict` object can also be dictionaries. For example:

```python
my_dict = gdict({
    'personal_info': {'name': 'Tom', 'age': 25},
    'work_info': {'company': 'ABC Inc.', 'position': 'Engineer'}
})
```

We can access and modify values in nested dictionaries:

```python
my_dict.personal_info.name  # 'Tom'
my_dict.work_info.position = 'Manager'
```

Aside from dot notation, we can also access and modify values in a `gdict` object using traditional dictionary access methods:

```python
my_dict['personal_info']['name']  # 'Tom'
my_dict['work_info']['position'] = 'Manager'
```

Lastly, the `gdict` class supports various input formats during instantiation:

```python
my_dict = gdict({'name': 'Tom', 'age': 25})
my_dict = gdict(name='Tom', age=25)
my_dict = gdict([('name', 'Tom'), ('age', 25)])
```

In summary, the design and implementation of the `gdict` class provide a convenient and extensible data structure that allows for more flexible manipulation of Python dictionary objects.
