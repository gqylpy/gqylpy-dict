"""
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

────────────────────────────────────────────────────────────────────────────────

Lines 51 through 95 is licensed under the Apache-2.0:

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

────────────────────────────────────────────────────────────────────────────────

All other code is licensed under the WTFPL:

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

────────────────────────────────────────────────────────────────────────────────
"""
import re
import sys
import builtins

from copy import copy, deepcopy

from typing import Type, Final, Optional, Union, Tuple, List, Hashable, Any

__unique__: Final = object()


class MasqueradeClass(type):
    """Masquerade one class as another.
    Warning, masquerade the class can cause unexpected problems, use caution."""
    __module__ = 'builtins'

    def __new__(mcs, __name__: str, __bases__: tuple, __dict__: dict):
        try:
            __masquerade_class__ = __dict__['__masquerade_class__']
        except KeyError:
            raise AttributeError(
                f'instance of "{mcs.__name__}" must '
                'define "__masquerade_class__" attribute, '
                'use to specify the class to disguise.'
            ) from None

        if not isinstance(__masquerade_class__, type):
            raise TypeError('"__masquerade_class__" is not a class.')

        cls = type.__new__(
            mcs, __masquerade_class__.__name__, __bases__, __dict__
        )

        mcs.__name__ = type.__name__
        cls.__module__ = __masquerade_class__.__module__

        # cls.__qualname__ = __masquerade_class__.__qualname__
        # Warning: Modify this attribute will cannot create the portable
        # serialized representation.

        if getattr(builtins, __masquerade_class__.__name__, None) is \
                __masquerade_class__:
            setattr(builtins, __name__, cls)

        return cls

    def __hash__(cls):
        if sys._getframe(1).f_code in (deepcopy.__code__, copy.__code__):
            return type.__hash__(cls)
        return hash(cls.__masquerade_class__)

    def __eq__(cls, o) -> bool:
        return True if o is cls.__masquerade_class__ else type.__eq__(cls, o)


builtins.MasqueradeClass = MasqueradeClass


class GqylpyDict(dict, metaclass=MasqueradeClass):
    __masquerade_class__ = dict
    __slots__ = ()

    def __init__(self, __data__=None, /, **data):
        if __data__ is None:
            __data__ = data
        else:
            __data__.update(data)

        for name, value in __data__.items():
            dict.__setitem__(self, name, GqylpyDict(value))

    def __new__(cls, __data__={}, /, **data):
        if isinstance(__data__, dict):
            return __data__ if __data__.__class__ is cls else dict.__new__(cls)

        if isinstance(__data__, (list, tuple, set, frozenset)):
            return __data__.__class__(cls(v) for v in __data__)

        return __data__

    def __getattr__(self, name: str, /) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any, /) -> None:
        self[name] = value

    def __delattr__(self, name: str, /) -> None:
        del self[name]

    def __setitem__(self, name: Hashable, value: Any, /) -> None:
        dict.__setitem__(self, name, GqylpyDict(value))

    def __hash__(self) -> int:
        return -2

    def __reduce__(self) -> Tuple[Type['GqylpyDict'], Tuple[dict]]:
        return GqylpyDict, (dict(self),)

    def copy(self) -> 'GqylpyDict':
        copied = GqylpyDict()
        for name, value in self.items():
            dict.__setitem__(copied, name, value)
        return copied

    def update(self, __data__: Optional[dict] = None, /, **data) -> None:
        try:
            dict.update(self, GqylpyDict(
                *() if __data__ is None else (__data__,), **data
            ))
        except (TypeError, ValueError):
            x: str = __data__.__class__.__name__
            raise TypeError(
                f'updated object must be a "dict", not "{x}".'
            ) from None

    def deepget(
            self,
            deepkey: str,
            /,
            default: Optional[Any]                = None,
            *,
            ignore:  Union[Tuple[Any], List[Any]] = ()
    ) -> Any:
        deepkey = deepkey[:-1] if deepkey and deepkey[-1] == ']' else deepkey
        value = self

        for key in re.split(r'\.|\[|][.\[]', deepkey):
            if isinstance(value, (list, tuple)):
                try:
                    key = int(key)
                except ValueError:
                    return default
            try:
                value = value[key]
            except KeyError:
                try:
                    if key.isdigit() or key[0] == '-' and key[1:].isdigit():
                        value = value[int(key)]
                    elif key in ('None', 'True', 'False', 'Ellipsis'):
                        value = value[eval(key)]
                    else:
                        return default
                except (KeyError, IndexError):
                    return default
            except (IndexError, TypeError):
                return default

        return default if value in ignore else value

    def deepset(self, deepkey: str, value: Any) -> None:
        existing_keys, nonexistent_keys = re.split(r'[.\[]', deepkey), []
        last_key: str = int_key(existing_keys.pop())

        while existing_keys:
            data = GqylpyDict.deepget(self, '.'.join(existing_keys), __unique__)
            # Why `GqylpyDict.deepget`? Compatible with built-in dict instance.

            key: str = int_key(existing_keys.pop())

            if data is not __unique__:
                try:
                    next_key = nonexistent_keys[0]
                except IndexError:
                    next_key = last_key
                if (
                        next_key.__class__ is str and not isinstance(data, dict)
                                                  or
                        next_key.__class__ is int and data.__class__ is not list
                ):
                    data = GqylpyDict.deepget(self, '.'.join(existing_keys)) \
                        if existing_keys else self
                    nonexistent_keys.insert(0, key)
                break
            nonexistent_keys.insert(0, key)
        else:
            data = self

        for i, key in enumerate(nonexistent_keys):
            try:
                next_key = nonexistent_keys[i + 1]
            except IndexError:
                next_key = last_key
            next_data = GqylpyDict() if next_key.__class__ is str else []
            data = set_next_data(data, key, next_data)
        set_next_data(data, last_key, value)

    def deepsetdefault(self, deepkey: str, default: Any) -> Any:
        value = GqylpyDict.deepget(self, deepkey, __unique__)
        if value is __unique__:
            GqylpyDict.deepset(self, deepkey, default)
            return default
        return value

    def deepcontain(self, deepkey: str, /) -> bool:
        return False if GqylpyDict.deepget(self, deepkey, __unique__) is \
                        __unique__ else True

    getdeep, setdeep = deepget, deepset

    __deepcopy__ = None
    # Compatible function `copy.deepcopy`.

    __isabstractmethod__ = False
    # Compatible metaclass `abc.ABCMeta`.


def int_key(key: str, /) -> Union[int, str]:
    try:
        return int(key[:-1])
    except ValueError:
        return key


def set_next_data(
        data:  Union[dict, list],
        key:   Union[int, str],
        value: Any
) -> Any:
    try:
        data[key] = value
    except IndexError:
        if key in (0, -1):
            data.append(value)
        elif key > 0:
            for _ in range(key - len(data)):
                data.append(None)
            data.append(value)
        else:
            for _ in range(abs(key) - len(data) - 1):
                data.append(None)
            data.insert(0, value)
    return data[key]
