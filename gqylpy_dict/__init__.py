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
__version__ = 1, 0, 'dev2'


class GqylpyDict(dict):
    """GqylpyDict == dict
    GqylpyDict equal dict, it's main function is to
    allow the dict to get or set values by `d.key`.
    """

    def __init__(self, *a, **kw):
        pass

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    @property
    def deepkeys(self) -> list:
        return self.get_deepkeys(self)

    @property
    def deepvalues(self) -> list:
        return self.get_deepvalues(self)

    @property
    def deepitems(self) -> list:
        return self.get_deepitems(self)

    def deepget(self, keypath: str, default: 'Any' = None, *, ignore: list = None) -> 'Any':
        """Get a value based on @param(keypath).
        @param keypath
            A key path, e.g.: {'a': [{'b': 'B'}]}.sget('a[0].b') == 'B'
        @param default
            If value not found based on @param(keypath), return @param(default).
        @param ignore
            If value in ignore based on @param(keypath), return @param(default).
        @return
            if value not found:
                return @param(default)
            if value in ignore:
                return @param(default)
            return value
        """

    def deepset(self, keypath: str, value: 'Any'):
        """Set @param(value) to self based on the @param(keypath).

        Example:
            from gqylpy_dict import gdict

            data = gdict({'a': [{'b': 'B'}]})
            data.deepset('a[0].c[0].d', 'D')

            print(data)
            # {'a': [{'b': 'B', 'c': [{'d': 'D'}]}]}
        """

    def deepsetdefault(self, keypath: str, value: 'Any') -> 'Any':
        """
        if @param(keypath) exists in self:
            return value based on @param(keypath)
        else:
            set the @param(value) to self based on @param(keypath)
            return @param(value)
        """

    def deepsetdefaultdict(self, defaultdict: dict):
        """Setdefault self from @param(defaultdict)."""

    def deepupdatedict(self, data: dict):
        """Update self from @param(data)."""

    def deepcontain(self, keypath: str) -> bool:
        """Return True if @param(keypath) exists in self else False."""

    @classmethod
    def get_deepkeys(cls, data: dict) -> list:
        """Get all keypath of @param(data)."""

    @classmethod
    def get_deepvalues(cls, data: dict) -> list:
        """Get all deep value of @param(data)."""

    @classmethod
    def get_deepitems(cls, data: dict) -> list:
        """Get all keypath and value of @param(data)."""

    @classmethod
    def get_deepvalue(cls, data: dict, keypath: str, default=None, *, ignore: list = None) -> 'Any':
        return cls.deepget(data, keypath, default, ignore=ignore)


class _______G________Q________Y_______L_______P_______Y_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']
    sys.modules[__name__].GqylpyDict = gcode.GqylpyDict


gdict = GqylpyDict

from typing import Any
