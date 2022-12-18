"""
Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

────────────────────────────────────────────────────────────────────────────────

Lines 48 through 96 is licensed under the Apache-2.0:

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
import builtins

from typing import Optional, Union, Tuple, Generator, Iterator, Any

unique = b'GQYLPY, \xe6\x94\xb9\xe5\x8f\x98\xe4\xb8\x96\xe7\x95\x8c\xe3\x80\x82'


class MasqueradeClass(type):
    """Masquerade one class as another.
    Warning: Masquerade the class can cause unexpected problems, use caution."""
    __module__ = 'builtins'

    def __new__(mcs, __name__: str, __bases__: tuple, __dict__: dict):
        try:
            __masquerade_class__ = __dict__['__masquerade_class__']
        except KeyError:
            raise AttributeError(
                f'an instance of "{mcs.__name__}" must '
                'define "__masquerade_class__" attribute, '
                'use to specify the class to disguise.'
            )

        if not isinstance(__masquerade_class__, type):
            raise TypeError('"__masquerade_class__" is not a class.')

        cls = type.__new__(
            mcs, __masquerade_class__.__name__, __bases__, __dict__
        )

        mcs.__name__ = type.__name__
        cls.__module__ = __masquerade_class__.__module__

        # cls.__qualname__ = __masquerade_class__.__qualname__
        # Warning: Modified this attribute will cannot
        # create the portable serialized representation.

        if getattr(builtins, __masquerade_class__.__name__, None) is \
                __masquerade_class__:
            setattr(builtins, __name__, cls)

        return cls

    def __str__(cls):
        return str(cls.__masquerade_class__)

    def __hash__(cls):
        # return hash(cls.__masquerade_class__)
        # Warning: If masquerade the hash value, will not get the
        # result from "copy.copy" and "copy.deepcopy" correctly.
        return super().__hash__()

    def __eq__(cls, o):
        return True if o is cls.__masquerade_class__ else super().__eq__(o)


builtins.MasqueradeClass = MasqueradeClass


class GqylpyDict(dict, metaclass=MasqueradeClass):
    __masquerade_class__ = dict
    __isabstractmethod__ = False
    __slots__ = ()

    def __init__(self, __data__=None, /, **kw):
        if isinstance(__data__, dict):
            kw and __data__.update(kw)
        else:
            __data__ = kw

        for name, value in __data__.items():
            self[name] = GqylpyDict(value)

    def __new__(cls, __data__={}, /, **kw):
        if isinstance(__data__, dict):
            return dict.__new__(cls)

        if isinstance(__data__, (list, tuple, set, frozenset, Iterator)):
            return [cls(v) for v in __data__]

        return __data__

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        del self[name]

    def __setitem__(self, name: Any, value: Any) -> None:
        dict.__setitem__(self, name, GqylpyDict(value))

    def __deepcopy__(self, memo=None) -> 'GqylpyDict':
        return GqylpyDict(self)

    def __hash__(self):
        return -2

    def __reduce__(self) -> Tuple[MasqueradeClass, dict]:
        return GqylpyDict, (dict(self),)

    def copy(self) -> 'GqylpyDict':
        x = GqylpyDict()
        for k, v in self.items():
            x[k] = v
        return x

    def update(self, __data__: dict = {}, /, **kw) -> None:
        try:
            super().update(GqylpyDict(__data__, **kw))
        except (TypeError, ValueError):
            x: str = __data__.__class__.__name__
            raise TypeError(f'updated object must be a "dict", not "{x}".')

    def deepget(
            self,
            keypath: str,
            /,
            default: Optional[Any]      = None,
            *,
            ignore:  Union[tuple, list] = ()
    ) -> Any:
        keypath = keypath[:-1] if keypath and keypath[-1] == ']' else keypath
        value = self

        for key in re.split(r'\.|\[|][.\[]', keypath):
            if value.__class__ is list:
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
                    elif key == 'None':
                        value = value[None]
                    else:
                        return default
                except (KeyError, IndexError):
                    return default
            except (IndexError, TypeError):
                return default

        return default if value in ignore else value

    def deepset(self, keypath: str, value: Any) -> None:
        existing_keys, nonexistent_keys = re.split(r'[.\[]', keypath), []
        last_key: str = int_key(existing_keys.pop())

        while existing_keys:
            data = GqylpyDict.deepget(self, '.'.join(existing_keys), unique)
            key: str = int_key(existing_keys.pop())

            if data is not unique:
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

    def deepsetdefault(self, keypath: str, value: Any) -> Any:
        result = self.deepget(keypath, unique)
        if result is unique:
            value = GqylpyDict(value)
            self.deepset(keypath, value)
            return value
        return result

    def deepcontain(self, keypath: str, /) -> bool:
        return False if self.deepget(keypath, unique) is unique else True

    def deepsetdefaultdict(self, defaultdict: dict, /) -> None:
        for key, value in self.get_deepitems(defaultdict):
            self.deepsetdefault(key, value)

    def deepupdatedict(self, data: dict, /) -> None:
        for key, value in self.get_deepitems(data):
            self.deepset(key, value)

    def deepkeys(self, __keypath__=None) -> Generator:
        for key, value in self.items():
            keypath = f'{__keypath__}.{key}' if __keypath__ else key

            if isinstance(value, dict):
                yield from GqylpyDict.deepkeys(value, keypath)
            elif isinstance(value, (list, tuple, set, Iterator)):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        yield from GqylpyDict.deepkeys(v, f'{keypath}[{i}]')
                    else:
                        yield f'{keypath}[{i}]'
            else:
                yield keypath

    def deepvalues(self, __keypath__=None) -> Generator:
        for key, value in self.items():
            keypath = f'{__keypath__}.{key}' if __keypath__ else key

            if isinstance(value, dict):
                yield from GqylpyDict.deepvalues(value, keypath)
            elif isinstance(value, (list, tuple, set, Iterator)):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        yield from GqylpyDict.deepvalues(v, f'{keypath}[{i}]')
                    else:
                        yield v
            else:
                yield value

    def deepitems(self, __keypath__=None) -> Generator:
        for key, value in self.items():
            keypath = f'{__keypath__}.{key}' if __keypath__ else key

            if isinstance(value, dict):
                yield from GqylpyDict.deepitems(value, keypath)
            elif isinstance(value, (list, tuple, set, Iterator)):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        yield from GqylpyDict.deepitems(v, f'{keypath}[{i}]')
                    else:
                        yield f'{keypath}[{i}]', v
            else:
                yield keypath, value

    @classmethod
    def getdeep(
            cls,
            data:    dict,
            keypath: str,
            default: Optional[Any]      = None,
            *,
            ignore:  Union[tuple, list] = ()
    ) -> Any:
        return cls.deepget(data, keypath, default, ignore=ignore)

    @classmethod
    def setdeep(cls, data: dict, keypath: str, value: Any) -> None:
        cls.deepset(data, keypath, value)

    @classmethod
    def keysdeep(cls, data: dict) -> Generator:
        return cls.deepkeys(data)

    @classmethod
    def valuesdeep(cls, data: dict) -> Generator:
        return cls.deepvalues(data)

    @classmethod
    def itemsdeep(cls, data: dict) -> Generator:
        return cls.deepitems(data)


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


try:
    from yaml.representer import Representer, SafeRepresenter
except ImportError:
    pass
else:
    def represent_gdict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data)
    Representer.add_representer(GqylpyDict, represent_gdict)
    SafeRepresenter.add_representer(GqylpyDict, represent_gdict)
