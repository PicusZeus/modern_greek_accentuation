from enum import Enum
from .resources import ULTIMATE, ANTEPENULTIMATE, PENULTIMATE
from typing import NewType


class Accent(Enum):
    ULTIMATE = ULTIMATE
    PENULTIMATE = PENULTIMATE
    ANTEPENULTIMATE = ANTEPENULTIMATE


AccentType = NewType('Accents', Accent)


def raise_type_exception(arg: any, _type: type):
    if type(arg) is not _type:
        raise TypeError(f"The argument must be of {_type.__qualname__} type")
