

run ``python -m doctest -v extra_tests.rst`` to test

Syllabification
==============

>>> from modern_greek_accentuation.syllabify import *

>>> modern_greek_syllabify('διαβατήριο')
['δια', 'βα', 'τή', 'ρι', 'ο']

>>> modern_greek_syllabify('Γεώργιος')
['Γιε', 'ωρ',  'γι', 'ος']