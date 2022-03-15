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

Copyright © 2022 GQYLPY. 竹永康 <gqylpy@outlook.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
from typing import Iterator

unique = 'b4526bbd82644a2db26dbd60b039c79d'


class HideClassInfo(type):
    __name__ = dict.__name__

    def __getattribute__(cls, name: str):
        if name == '__class__':
            return dict.__class__
        # Masquerading as a built-in thing will not serialize properly.
        if name == '__module__':
            return dict.__module__
        return super().__getattribute__(name)

    def __str__(cls) -> str:
        return str(dict)


class GqylpyDict(dict, metaclass=HideClassInfo):

    __isabstractmethod__ = False
    # The attribute is for compatibility abc.ABCMeta.

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

        if __data__.__class__ in (list, Iterator, tuple, set):
            return [GqylpyDict(v) for v in __data__]

        return __data__

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __deepcopy__(self, memo):
        """
        This method must be implemented,  otherwise
        `KeyError: '__deepcopy__'` will appear when
        `copy.deepcopy (GqylpyDict obj)` is called.
        """
        return GqylpyDict(self)

    def __getstate__(self):
        """This method is for compatibility pickle module."""
        return self

    def __setstate__(self, state):
        """This method is for compatibility pickle module."""

    def __hash__(self):
        return -1

    def __eq__(self, other):
        return super().__eq__(other)

    def update(self, __data__: dict = None, **kw):
        if isinstance(__data__, dict):
            kw and __data__.update(kw)
        elif __data__ is None:
            _data = kw
        else:
            x: str = __data__.__class__.__name__
            raise TypeError(f'Updated object must be "dict", not a "{x}".')

        if not isinstance(__data__, GqylpyDict):
            __data__ = GqylpyDict(__data__)

        super().update(__data__)

    @property
    def deepkeys(self) -> list:
        return self.get_deepkeys(self)

    @property
    def deepvalues(self) -> list:
        return self.get_deepvalues(self)

    @property
    def deepitems(self) -> list:
        return self.get_deepitems(self)

    def deepget(self, keypath: str, default=None, *, ignore: list = []):
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
            data = self.deepget('.'.join(yes_keys), unique)
            key: str = int_key(yes_keys.pop())

            if data != unique:
                try:
                    next_key = no_keys[0]
                except IndexError:
                    next_key = last_key
                if next_key.__class__ is str and data.__class__ is not GqylpyDict \
                        or next_key.__class__ is int and data.__class__ is not list:
                    data = self.deepget('.'.join(yes_keys)) if yes_keys else self
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

    def deepsetdefault(self, keypath: str, value):
        result = self.deepget(keypath, unique)
        if result == unique:
            self.deepset(keypath, value)
            return value
        return result

    def deepsetdefaultdict(self, defaultdict: dict):
        for key, value in self.get_deepitems(defaultdict):
            self.deepsetdefault(key, value)

    def deepupdatedict(self, data: dict):
        for key, value in self.get_deepitems(data):
            self.deepset(key, value)

    def deepcontain(self, keypath: str) -> bool:
        return True if self.deepget(keypath, unique) != unique else False

    @classmethod
    def get_deepkeys(cls, data: dict, _keypath: str = None, _keypaths: list = None) -> list:
        keypaths = _keypaths or []

        for key, value in data.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

            if isinstance(value, dict):
                cls.get_deepkeys(value, keypath, keypaths)
            elif value.__class__ in (list, Iterator, tuple, set):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        cls.get_deepkeys(v, f'{keypath}[{i}]', keypaths)
                    else:
                        keypaths.append(f'{keypath}[{i}]')
            else:
                keypaths.append(keypath)

        return keypaths

    @classmethod
    def get_deepvalues(cls, data: dict, _keypath: str = None, _keypaths: list = None) -> list:
        keypaths = _keypaths or []

        for key, value in data.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

            if isinstance(value, dict):
                cls.get_deepvalues(value, keypath, keypaths)
            elif value.__class__ in (list, Iterator, tuple, set):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        cls.get_deepvalues(v, f'{keypath}[{i}]', keypaths)
                    else:
                        keypaths.append(v)
            else:
                keypaths.append(value)

        return keypaths

    @classmethod
    def get_deepitems(cls, data: dict, _keypath: str = None, _keypaths: list = None) -> list:
        keypaths = _keypaths or []

        for key, value in data.items():
            keypath = f'{_keypath}.{key}' if _keypath else key

            if isinstance(value, dict):
                cls.get_deepitems(value, keypath, keypaths)
            elif value.__class__ in (list, Iterator, tuple, set):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        cls.get_deepitems(v, f'{keypath}[{i}]', keypaths)
                    else:
                        keypaths.append((f'{keypath}[{i}]', v))
            else:
                keypaths.append((keypath, value))

        return keypaths

    @classmethod
    def get_deepvalue(cls, data: dict, keypath: str, default=None, *, ignore: list = []):
        return cls.deepget(data, keypath, default, ignore=ignore)


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
