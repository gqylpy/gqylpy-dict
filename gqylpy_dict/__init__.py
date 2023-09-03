"""
The `gqylpy_dict` based on the built-in `dict`, it is an enhancement of the
built-in `dict`. It can do anything `dict` can do, and can do more what `dict`
cannot do.

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

    @version: 1.2.5
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-dict

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

This file is licensed under the WTFPL:

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""
from typing import Optional, Union, Tuple, List, Hashable, Any


class gdict(dict):
    """
    The `gdict` class is a custom dictionary class that inherits from the
    built-in Python `dict` class. One unique feature of the gdict class is that
    it supports accessing and modifying key-value pairs in the dictionary using
    dot notation ('.'). This means we can access values in the dictionary like
    we would access attributes of an object. For example, given a dictionary
    `{'name': 'Tom', 'age': 25}`, we can create a gdict object as follows:

        >>> my_dict = gdict({'name': 'Tom', 'age': 25})

    Using dot notation, we can access values in this dictionary:

        >>> my_dict.name
        'Tom'
        >>> my_dict.age
        25

    We can even modify values in this dictionary using dot notation:

        >>> my_dict.name = 'Jerry'

    Now, the value of the "name" key in this dictionary has been updated to
    "Jerry".

    Additionally, `gdict` supports nested data structures, meaning the keys and
    values stored in a `gdict` object can be dictionaries themselves. For
    example:

        >>> my_dict = gdict({
        >>>     'personal_info': {'name': 'Tom', 'age': 25},
        >>>     'work_info': {'company': 'ABC Inc.', 'position': 'Engineer'}
        >>> })

    We can access and modify values in nested dictionaries:

        >>> my_dict.personal_info.name
        'Tom'
        >>> my_dict.work_info.position = 'Manager'

    In addition to dot notation, we can also access and modify values in `gdict`
    objects using traditional dictionary syntax:

        >>> my_dict['personal_info']['name']
        'Tom'
        >>> my_dict['work_info']['position'] = 'Manager'

    Finally, the `gdict` class has multiple input formats when instantiating an
    object:

        >>> my_dict = gdict({'name': 'Tom', 'age': 25})
        >>> my_dict = gdict(name='Tom', age=25)
        >>> my_dict = gdict([('name', 'Tom'), ('age', 25)])

    The above is the main functions and usage of the `gdict` class. Overall, the
    design and implementation of the `gdict` class provide a convenient and
    extensible data structure that allows greater flexibility for operating on
    Python dictionary objects.
    """

    def __new__(cls, __data__={}, /, **data):
        """
        When we create a new `gdict` object, the class actually initializes a
        Python `dict`. The initial value can be passed in as a constructor
        parameter (which can be a `dict`, `list`, `tuple`, or other data type)
        or passed in as keyword arguments.

        The `gdict` class overrides the `__new__` and `__init__` methods, which
        are responsible for accepting the constructor parameters and converting
        them into `gdict` objects. The `__new__` method implements type checking
        on the passed-in parameters, returning a new `dict` if it is a `dict`,
        converting each element of a `list` or `tuple` into a `gdict` type and
        returning a new `list` or `tuple`, or returning the data directly if it
        is another data type. For other data types, we can also use keyword
        arguments to pass them as initial values.

        The `__init__` method accepts the newly converted `dict` and iterates
        over each key-value pair, using the `__setitem__` method to add them to
        the `dict`. In the `__setitem__` method, we use `value = gdict(value)`
        to set the value as a `gdict` object, so that nested `gdict` objects are
        created recursively when needed.

        In this way, we can create a nested `gdict` of any level, with each
        inner dictionary being a `gdict` object, thereby achieving the
        conversion of any nested `dict`.
        """
        if isinstance(__data__, dict):
            return dict.__new__(cls)

        if isinstance(__data__, (list, tuple)):
            return __data__.__class__(cls(v) for v in __data__)

        return __data__

    def __init__(self, __data__=None, /, **data):
        if __data__ is None:
            __data__ = data
        else:
            __data__.update(data)

        for key, value in __data__.items():
            dict.__setitem__(self, key, gdict(value))

    def __getattr__(self, key: str, /) -> Any:
        return self[key]

    def __setattr__(self, key: str, value: Any, /) -> None:
        self[key] = value

    def __delattr__(self, key: str, /) -> None:
        del self[key]

    def __setitem__(self, key: Hashable, value: Any, /) -> None:
        if not isinstance(value, gdict):
            value = gdict(value)
        dict.__setitem__(self, key, value)

    def __hash__(self) -> int:
        """
        The first thing you have to understand is that the built-in dict object
        is unhashable. Don't be misled!

        We do this mainly so that instances of `GqylpyDict` can be able to be
        added to instance of `set`. Ignore the hash check and always check that
        the values are equal.

        Backstory https://github.com/gqylpy/gqylpy-dict/issues/7
        """
        return -2

    def copy(self) -> 'gdict':
        """Get a replica instance."""

    def deepcopy(self) -> 'gdict':
        """
        Incomplete deep copy, NOTE not the same as `copy.deepcopy`!

        Copy only the instances of container types (only instances of `gdict`,
        `dict`, `list` and `tuple`).

        Backstory https://github.com/gqylpy/gqylpy-dict/issues/9
        """
        return gdict(self)

    def deepget(
            self,
            deepkey: str,
            /,
            default: Optional[Any]                          = None,
            *,
            ignore:  Optional[Union[Tuple[Any], List[Any]]] = None
    ) -> Any:
        """
        Try to get a depth value, if not then return the default value.

            >>> x = gdict({'a': [{'b': 'B'}]})
            >>> x.deepget('a[0].b')
            'B'

        @param deepkey
            Hierarchical keys, use "." join, if the next layer is an array then
            use the index number to join.

        @param default
            If not get the depth value then return the default value.

        @param ignore
            Use tuple or list to specify one or more undesired values, if the
            depth value is in it then return the default value. This parameter
            may be removed in the future.
        """

    def deepset(self, deepkey: str, value: Any) -> None:
        """
        Set a depth value (to the depth key), overwrite if exists.

            >>> x = gdict()
            >>> x.deepset('a[1].b', 'B')
            >>> x
            {'a': [None, {'b': 'B'}]}

        @param deepkey
            Hierarchical keys, use "." join, if the next layer is an array then
            use the index number to join.

        @param value
            Pass in any value, will be set to the value of the depth key,
            overwrite if exists.
        """

    def deepsetdefault(self, deepkey: str, default: Any) -> Any:
        """
        If the depth key does not exist then set the default value and return
        it, otherwise return the value of the depth key.

            >>> x = gdict()
            >>> x.deepsetdefault('a[0].b', 'B')
            'B'
            >>> x
            {'a': [{'b': 'B'}]}

        @param deepkey
            Hierarchical keys, use "." join, if the next layer is an array then
            use the index number to join.

        @param default
            Pass in any value, will be set to the value of the depth key if the
            depth key does not exist.
        """

    def deepcontain(self, deepkey: str, /) -> bool:
        """
        Return True if the depth key exists else False.

        >>> x = gdict({'a': [{'b': 'B'}]})
        >>> x.deepcontain('a[0].b')
        True
        >>> x.deepcontain('a[1].b')
        False

        @param deepkey
            Hierarchical keys, use "." join, if the next layer is an array then
            use the index number to join.
        """

    @classmethod
    def getdeep(
            cls,
            data:    dict,
            deepkey: str,
            /,
            default: Optional[Any]                          = None,
            *,
            ignore:  Optional[Union[Tuple[Any], List[Any]]] = None
    ) -> Any:
        """
        The `getdeep` based on `deepget`, and is provided for built-in `dict`.
        If you want to use `deepget` but don't want to or can't give up the
        original data, can use `getdeep`.
        """
        warnings.warn(
            f'will be deprecated soon, replaced to {cls.deepget}.',
            DeprecationWarning
        )
        return cls.deepget(data, deepkey, default, ignore=ignore)

    @classmethod
    def setdeep(cls, data: dict, deepkey: str, value: Any) -> None:
        """
        The `setdeep` based on `deepset`, and is provided for built-in `dict`.
        If you want to use `deepset` but don't want to or can't give up the
        original data, can use `setdeep`.
        """
        warnings.warn(
            f'will be deprecated soon, replaced to {cls.deepset}.',
            DeprecationWarning
        )
        cls.deepset(data, deepkey, value)


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    gdict = __import__(f'{__name__}.g {__name__[7:]}', fromlist=...).GqylpyDict

    for gname, gvalue in globals().items():
        if gname[0] == '_' and gname != '__name__':
            setattr(gdict, gname, gvalue)

    sys.modules[__name__] = gdict.gdict = gdict
