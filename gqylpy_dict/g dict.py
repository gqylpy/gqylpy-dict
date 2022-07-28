"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

─────────────────────────────────────────────────────────────────────────────────────────────────────

Lines 61 through 101 is licensed under the Apache-2.0:

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

─────────────────────────────────────────────────────────────────────────────────────────────────────

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
─────────────────────────────────────────────────────────────────────────────────────────────────────
"""
import re
import builtins

from typing import Iterator, Any, Union, NoReturn, Optional

unique = b'GQYLPY, \xe6\x94\xb9\xe5\x8f\x98\xe4\xb8\x96\xe7\x95\x8c\xe3\x80\x82'


class DisguiseClass(type):
    __module__ = 'builtins'

    def __new__(mcs, __name__: str, __bases__: tuple, __dict__: dict):
        try:
            __disguise_class__: type = __dict__['__disguise_class__']
        except KeyError:
            raise AttributeError(
                f'an instance of "{mcs.__name__}" must '
                'define "__disguise_class__" attribute, '
                'use to specify the class to disguise.'
            )

        if not isinstance(__disguise_class__, type):
            raise TypeError(f'"__disguise_class__" is not a class.')

        cls = type.__new__(mcs, __disguise_class__.__name__, __bases__, __dict__)

        mcs.__name__ = type.__name__
        cls.__module__ = __disguise_class__.__module__

        # Warning: modifying this property will not create a portable serialized representation.
        # cls.__qualname__ = __disguise_class__.__qualname__
        # _pickle.PicklingError: Can't pickle <class 'dict'>: it's not the same object as builtins.dict

        if getattr(builtins, __disguise_class__.__name__, None) is __disguise_class__:
            setattr(builtins, __name__, cls)

        return cls

    def __str__(cls) -> str:
        return str(cls.__disguise_class__)

    def __hash__(cls):
        return hash(cls.__disguise_class__)

    def __eq__(cls, o):
        return True if o is cls.__disguise_class__ else super().__eq__(o)


builtins.DisguiseClass = DisguiseClass


class GqylpyDict(dict, metaclass=DisguiseClass):
    __disguise_class__ = dict

    def __init__(self, __data__=None, **kw):
        if __data__.__class__ is dict:
            kw and __data__.update(kw)
        else:
            __data__ = kw

        for name, value in __data__.items():
            self[name] = GqylpyDict(value)

    def __new__(cls, __data__={}, **kw):
        if __data__.__class__ is dict:
            return dict.__new__(cls)

        if isinstance(__data__, (list, tuple, set, Iterator)):
            return [GqylpyDict(v) for v in __data__]

        return __data__

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __deepcopy__(self, memo):
        return GqylpyDict(self)

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        pass

    def __hash__(self):
        return -2

    def update(self, __data__: dict = None, **kw):
        if isinstance(__data__, dict):
            kw and __data__.update(kw)
        elif __data__ is None:
            _data = kw
        else:
            x: str = __data__.__class__.__name__
            raise TypeError(f'updated object must be a "dict", not "{x}".')

        if __data__.__class__ is not GqylpyDict:
            __data__ = GqylpyDict(__data__)

        super().update(__data__)

    def deepget(self, keypath: str, default=None, *, ignore: tuple = ()):
        value, keypath = self, keypath[:-1] if keypath and keypath[-1] == ']' else keypath

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

    def deepset(self, keypath: str, value):
        yes_keys, no_keys = re.split(r'[.\[]', keypath), []
        last_key: str = int_key(yes_keys.pop())

        while yes_keys:
            data = GqylpyDict.deepget(self, '.'.join(yes_keys), unique)
            key: str = int_key(yes_keys.pop())

            if data is not unique:
                try:
                    next_key = no_keys[0]
                except IndexError:
                    next_key = last_key
                if next_key.__class__ is str and data.__class__ is not GqylpyDict \
                        or next_key.__class__ is int and data.__class__ is not list:
                    data = GqylpyDict.deepget(self, '.'.join(yes_keys)) if yes_keys else self
                    no_keys.insert(0, key)
                break
            no_keys.insert(0, key)
        else:
            data = self

        for i, key in enumerate(no_keys):
            try:
                next_key = no_keys[i + 1]
            except IndexError:
                next_key = last_key
            next_data = GqylpyDict() if next_key.__class__ is str else []
            set_next_data(data, key, next_data)
            data = next_data
        set_next_data(data, last_key, value)

    def deepcontain(self, keypath: str) -> bool:
        return False if self.deepget(keypath, unique) is unique else True

    def deepsetdefault(self, keypath: str, value):
        result = self.deepget(keypath, unique)
        if result is unique:
            value = GqylpyDict(value)
            self.deepset(keypath, value)
            return value
        return result

    def deepsetdefaultdict(self, defaultdict: dict):
        for key, value in self.get_deepitems(defaultdict):
            self.deepsetdefault(key, value)

    def deepupdatedict(self, data: dict):
        for key, value in self.get_deepitems(data):
            self.deepset(key, value)

    def deepkeys(self, _keypath: str = None):
        for key, value in self.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

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

    def deepvalues(self, _keypath: str = None):
        for key, value in self.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

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

    def deepitems(self, _keypath: str = None):
        for key, value in self.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

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
    def get_deepkeys(cls, data: dict):
        return cls.deepkeys(data)

    @classmethod
    def get_deepvalues(cls, data: dict):
        return cls.deepvalues(data)

    @classmethod
    def get_deepitems(cls, data: dict):
        return cls.deepitems(data)

    @classmethod
    def get_deepvalue(cls, data: dict, keypath: str, default=None, *, ignore: tuple = ()):
        return cls.deepget(data, keypath, default, ignore=ignore)

    @classmethod
    def set_deepvalue(cls, data: dict, keypath: str, value):
        cls.deepset(data, keypath, value)

    __isabstractmethod__ = False
    # Compatibility with "abc.ABCMeta".


def int_key(key: str) -> str or int:
    try:
        return int(key[:-1])
    except ValueError:
        return key


def set_next_data(data: dict or list, key: str or int, value):
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
