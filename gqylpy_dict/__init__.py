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

    @version: 1.2
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

    def __new__(cls, __data__={}, /, **data):
        if isinstance(__data__, dict):
            return __data__ if __data__.__class__ is cls else dict.__new__(cls)

        if isinstance(__data__, (list, tuple, set, frozenset)):
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
        dict.__setitem__(self, key, gdict(value))

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

    __import__(f'{__name__}.g {__name__[7:]}')
    gdict = globals()[f'g {__name__[7:]}'].GqylpyDict

    for gname in globals():
        if gname[0] == '_' and gname != '__name__':
            setattr(gdict, gname, globals()[gname])

    sys.modules[__name__] = gdict.gdict = gdict
