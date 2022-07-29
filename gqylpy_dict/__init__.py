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
__version__ = 1, 0, 'alpha4'
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-dict'


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

    def copy(self) -> 'GqylpyDict':
        pass

    def deepkeys(self) -> list:
        return self.get_deepkeys(self)

    def deepvalues(self) -> list:
        return self.get_deepvalues(self)

    def deepitems(self) -> list:
        return self.get_deepitems(self)

    def deepget(self, keypath: str, default: 'Any' = None, *, ignore: 'Union[tuple, list]' = None) -> 'Any':
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
    def get_deepvalue(cls, data: dict, keypath: str, default=None, *, ignore: 'Union[tuple, list]' = None) -> 'Any':
        return cls.deepget(data, keypath, default, ignore=ignore)

    @classmethod
    def set_deepvalue(cls, data: dict, keypath: str, value):
        cls.deepset(data, keypath, value)


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']
    sys.modules[__name__].GqylpyDict = gcode.GqylpyDict


gdict = GqylpyDict

from typing import Any, Union
