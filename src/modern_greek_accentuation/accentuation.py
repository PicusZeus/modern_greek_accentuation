from __future__ import annotations

from _ctypes_test import func
from _testcapi import raise_exception

from modern_greek_accentuation._helpers import raise_type_exception, AccentType
from modern_greek_accentuation.syllabify import *
from modern_greek_accentuation.resources import PENULTIMATE, ANTEPENULTIMATE, ULTIMATE, INCORRECT_ACCENT
import unicodedata

"""
**It is highly recommended to use in the below functions accent variables instead of strings. You can import them from resource module**
`from modern_greek_accentuation.resources import PENULTIMATE, ANTEPENULTIMATE, ULTIMATE, INCORRECT_ACCENT`
"""

def remove_diacritics(*diacritics: list[str], diaeresis: bool = True) -> func:

    """
    **Factory function for customizing functions that remove accents.**

    *Even though Modern Greek has officially monotonic writing, there can be still instances of polytonic texts, so all diacritics which are known from ancient language, can be included.*

    :param diacritics: List of diacritics to be removed, these are the possiblities: PSILI, DASIA, OXIA, VARIA, PERISPOMENI, YPOGEGRAMMENI, DIAERESIS (import them from `resource` module).
    :param diaeresis: If dieresis is set to True, it checks if dieresis is expected because of accent position and in such a case dieresis is added.
    :return: Function that will remove diacritics that were set as *args from a given string.
    """

    def _(text: str, dieresis=diaeresis) -> str:
        if dieresis:
            dieresis_dipht = {'όι': 'οϊ', "άι": 'αϊ', "έι": 'εϊ', 'ύι': 'υϊ', 'όυ': 'οϋ'}
            for d in dieresis_dipht.keys():
                if d in text:
                    text = text.replace(d, dieresis_dipht[d])
        return unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFD", text)
                                                    if ch not in diacritics))

    return _


remove_all_accents = remove_diacritics(CIRCUMFLEX, ACUTE, GRAVE, diaeresis=True)
"""
Remove all accent marks and leave everythin else.
"""

remove_all_diacritics = remove_diacritics(PSILI, DASIA, OXIA, VARIA, PERISPOMENI, YPOGEGRAMMENI)
"""
Remove all diacritics.
"""
#

remove_all_diacritics_with_dier = remove_diacritics(PSILI, DASIA, OXIA, VARIA, PERISPOMENI, YPOGEGRAMMENI, DIAERESIS)
"""
Remove all diacritics but dieresis
"""
#

remove_non_accent_diacritics = remove_diacritics(YPOGEGRAMMENI, ROUGH, SMOOTH)
"""
Remove both breathing marks and iota subscriptum
"""
#

remove_non_accent_diacritics_without_dieresis = remove_diacritics(YPOGEGRAMMENI, ROUGH, SMOOTH, diaeresis=False)
"""
Remove both breathing marks and iota subscriptum but leaves dieresis
"""
#

remove_diaer = remove_diacritics(DIAERESIS)
"""
Remove only dieresis
"""
#


def convert_to_monotonic(sentence_or_word: str, one_syllable_rule: bool = True) -> str:
    """
    **Converts text in polytonic system to monotonic.**

    :param sentence_or_word: Greek text of whatever length.
    :param one_syllable_rule: If set to True, accent is removed from all single syllable words with some basic exceptions (like interrogative pronouns in questions).
    :return: Text converted to monotonic accentuation system.
    """
    raise_type_exception(sentence_or_word, str)

    sentence_or_word = remove_non_accent_diacritics_without_dieresis(sentence_or_word)
    sentence_or_word = unicodedata.normalize("NFD", sentence_or_word)
    for polytonic_accent in [VARIA, PERISPOMENI]:
        sentence_or_word = sentence_or_word.replace(polytonic_accent, OXIA)
    sentence_or_word = unicodedata.normalize("NFC", "".join(sentence_or_word))
    words = sentence_or_word.split()
    removed_one_syllable_accent = []
    excluded = ['ή']
    if sentence_or_word[-1] == ';':
        excluded = ['ή', 'πού', 'πώς']
    for word in words:
        if one_syllable_rule:
            if count_syllables(word) == 1 and word not in excluded:
                removed_one_syllable_accent.append(remove_all_diacritics(word))
            else:
                removed_one_syllable_accent.append(word)
        else:
            return ' '.join(words)

    return ' '.join(removed_one_syllable_accent)


def is_accented(syllable: str) -> bool:
    """
    :param syllable: A single syllable.
    :return: True if accented, otherwise false.
    """
    raise_type_exception(syllable, str)

    if type(syllable) is not str:
        raise TypeError

    for ch in unicodedata.normalize("NFD", syllable):
        if ch in [VARIA, OXIA, PERISPOMENI]:
            return True

    return False


def has_multiple_accents(word: str) -> bool:
    """
    :param word: a single word
    :return: if a word has more than one accent, return True, else False.
    """
    raise_type_exception(word, str)

    number_of_accents = 0
    for syllable in modern_greek_syllabify(word):
        if is_accented(syllable):
            number_of_accents += 1

        if number_of_accents > 1:
            return True

    return False


def put_accent_on_a_vowel(vowel: str) -> str:
    """
    :param vowel: a single vowel
    :return: a vowel with the acute, if there is diaeresis on vowel, diaeresis stays, and if there were polytonic accents, they are replaced with the acute accent.
    """
    raise_type_exception(vowel, str)

    vowel = remove_all_diacritics(vowel)
    if not vowel in vowels:
        return vowel

    return unicodedata.normalize("NFC", "".join((vowel, OXIA)))


def put_accent_on_syllable(syllable: str) -> str:
    """
    :param syllable: A single syllable, already accented or not.
    :return: An accented with the acute accent syllable
    """
    raise_type_exception(syllable, str)

    accented_syllable = None

    for def_diph in list_of_def_diphthongs:
        # since 'i' can be treated as a consonant before other vowels, we need to check if this is the case
        if def_diph in syllable:
            accented_def_diph = def_diph[:-1] + put_accent_on_syllable(def_diph[-1])
            syllable = syllable.replace(def_diph, accented_def_diph)
            accented_syllable = syllable
            break

    if not accented_syllable:
        for diph in diphtongs:

            if diph in syllable:
                accented_diphtong = diph[0] + put_accent_on_a_vowel(diph[1])
                syllable = syllable.replace(diph, accented_diphtong)
                accented_syllable = syllable
                break
    if not accented_syllable:
        for vow in vowels:
            if vow in syllable:
                syllable = syllable.replace(vow, put_accent_on_a_vowel(vow))
                accented_syllable = syllable
                break

    # but if accent makes diaeresis redundant, it should be removed
    accented_syllable = remove_redundand_diaeresis(accented_syllable)

    return accented_syllable


def where_is_accent(word: str, true_syllabification=True) -> AccentType | None:
    """
    **This function will tell you where is the accent.**

    :param word: a single word
    :param true_syllabification: unaccented "i" before vowels or after certain vowels is not treated as a vowel if set to True (sinizisi).
    :return: ANTEPENULTIMATE, PENULTIMATE, ULTIMATE, INCORRECT_ACCENT, and if there is no accent, None
    """
    raise_type_exception(word, str)

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)
    accent = 100
    syllables = reversed(syllables)
    for (index, syllable) in enumerate(syllables):
        if is_accented(syllable):
            accent = index
            break
    if accent == 100:
        return None
    elif accent == 0:
        return ULTIMATE
    elif accent == 1:
        return PENULTIMATE
    elif accent == 2:
        return ANTEPENULTIMATE
    else:
        return INCORRECT_ACCENT


def put_accent(word: str, accent_name: AccentType, true_syllabification=True) -> str:
    """
    **This function allows you to put a given accent on a word**

    :param word: a single word, which can be already accented
    :param accent_name: ANTEPENULTIMATE, PENULTIMATE, ULTIMATE
    :param true_syllabification: unaccented "i" after consonants is not treated as vowel if set to True (sinizisi).
    :return: if accent_name param given incorrect, return input word, else return a word with a prescribed accent.
    """
    if accent_name == ULTIMATE:
        word = put_accent_on_the_ultimate(word, true_syllabification=true_syllabification)
    elif accent_name == PENULTIMATE:

        word = put_accent_on_the_penultimate(word, true_syllabification=true_syllabification)
    elif accent_name == ANTEPENULTIMATE:
        word = put_accent_on_the_antepenultimate(word, true_syllabification=true_syllabification)

    return word


def remove_redundand_diaeresis(word: str) -> str:
    """
    :param word: A single word
    :return: If dieresis is not needed because position of an accent makes it superfluous, a word without dieresis.
    """
    redundant_diaereseis = {'όϊ': 'όι', 'άϊ': "άι", 'έϊ': "έι", 'ύϊ': 'ύι', 'όϋ': 'όυ'}
    if DIAERESIS in unicodedata.normalize('NFD', word):
        for redundant_diaeresis in redundant_diaereseis:
            if redundant_diaeresis in word:
                word = word.replace(redundant_diaeresis, redundant_diaereseis[redundant_diaeresis])
                break
    return word


def put_accent_on_the_ultimate(word: str, accent_one_syllable=True, second_accent=False, true_syllabification=True) -> str | None:
    """
    **This functions put accent on the ultimate syllable in a given word**

    :param word: A single word.
    :param accent_one_syllable:  If set to True, accent is removed from all single syllable words with some basic exceptions (like interrogative pronouns in questions).
    :param second_accent: If there is already accent on antepenultimate and this flag is set to True, second accent will be added to a single word.
    :param true_syllabification: Unaccented "i" after consonants is not treated as vowel if set to True (sinizisi).
    :return: The word with an accent on the ultimate.
    """

    if second_accent:
        if where_is_accent(
                word, true_syllabification=False
        ) == ANTEPENULTIMATE:
            pass
        else:

            word = remove_all_diacritics(word)
    else:
        word = remove_all_diacritics(word)

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    if not accent_one_syllable and len(syllables) < 2:
        return remove_all_diacritics(word)

    to_be_accented = syllables[-1]
    accented = put_accent_on_syllable(to_be_accented)

    if accented:
        syllables[-1] = accented
        res = ''.join(syllables)

        return res
    else:
        return None


def put_accent_on_the_penultimate(word: str, true_syllabification=True) -> str:
    """
    **This functions put accent on the penultimate syllable in a given word**
    :param word: A single word.
    :param true_syllabification: unaccented "i" after consonants is not treated as vowel if set to True (sinizisi).
    :return: The word with an accent on the penultimate.

    """
    # if one syllable, do not put any accent
    word = remove_all_diacritics(word)
    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    if len(syllables) > 1:
        to_be_accented = syllables[-2]
        accented = put_accent_on_syllable(to_be_accented)

        syllables[-2] = accented
        res = ''.join(syllables)

        res = remove_redundand_diaeresis(res)

        return res
    else:
        return word


def put_accent_on_the_antepenultimate(word: str, true_syllabification=True) -> str:
    """
    **This functions put accent on the antepenultimate syllable in a given word**

    :param word: A single word.
    :param true_syllabification: unaccented "i" after consonants is not treated as vowel if set to True (sinizisi).
    :return: The word with an accent on the antepenultimate.
    """
    # if one syllable word given, doesnt put accent

    word = remove_all_diacritics(word)

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    # if word is accented on ult, antepenult is still possible
    if len(syllables) > 2:

        to_be_accented = syllables[-3]

        accented = put_accent_on_syllable(to_be_accented)

        syllables[-3] = accented
        res = ''.join(syllables)
        res = remove_redundand_diaeresis(res)
        return res
    else:
        res = put_accent_on_the_penultimate(word)

    return res
