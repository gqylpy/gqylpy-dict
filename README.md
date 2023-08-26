[<img alt='LOGO' src='http://gqylpy.com/static/img/favicon.ico' height='21' width='21'/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-dict.svg?style=flat-square')](https://github.com/gqylpy/gqylpy-dict/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_dict)](https://pypi.org/project/gqylpy_dict)
[![License](https://img.shields.io/pypi/l/gqylpy_dict)](https://github.com/gqylpy/gqylpy-dict/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/gqylpy_dict)](https://pepy.tech/project/gqylpy_dict)

# gqylpy-dict

> `gqylpy-dict` 基于内置 `dict`，它是对内置 `dict` 的增强。内置 `dict` 能做的它都能做，内置 `dict` 不能做的它更能做。_（专为神经患者设计）_

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

我们再详细地介绍一下 `gdict` 类的功能和用法。

首先，`gdict` 类是一个自定义字典类，继承自 Python 内置的 `dict` 类。`gdict` 类有一个特殊的功能是支持点操作符（`.`）访问和修改字典中的键值对。这意味着，我们可以像访问对象的属性一样访问字典中的值。比如，有一个字典 `{'name': 'Tom', 'age': 25}`，我们可以这样定义一个 `gdict` 对象：
```python
my_dict = gdict({'name': 'Tom', 'age': 25})
```

通过点操作符，我们可以访问这个字典的值：
```python
my_dict.name  # 'Tom'
my_dict.age  # 25
```

我们甚至可以修改这个字典的值：
```python
my_dict.name = 'Jerry'
```
此时，这个字典中 `'name'` 这个键对应的值已经被修改为 `'Jerry'`。

另外，`gdict` 还支持多层嵌套的数据结构，也就是说，`gdict` 对象中存储的键和值也可以是字典类型。比如：
```python
my_dict = gdict({
    'personal_info': {'name': 'Tom', 'age': 25},
    'work_info': {'company': 'ABC Inc.', 'position': 'Engineer'}
})
```

我们可以访问和修改嵌套字典中的值：
```python
my_dict.personal_info.name  # 'Tom'
my_dict.work_info.position = 'Manager'
```

除了点操作符，我们也可以使用普通的字典操作方式访问和修改 `gdict` 对象中的值：
```python
my_dict['personal_info']['name']  # 'Tom'
my_dict['work_info']['position'] = 'Manager'
```

最后，`gdict` 类在实例化时支持多种不同的输入方式：
```python
my_dict = gdict({'name': 'Tom', 'age': 25})
my_dict = gdict(name='Tom', age=25)
my_dict = gdict([('name', 'Tom'), ('age', 25)])
```

以上就是 `gdict` 类的主要功能和用法。总体来说，`gdict` 类的设计和实现提供了一种方便的、可扩展的数据结构，可以更加灵活地操作 Python 字典对象。
