from __future__ import annotations

from _ctypes_test import func

from modern_greek_accentuation.syllabify import *

import unicodedata


def remove_diacritics(*diacritics: list[str], diaeresis: bool = True) -> func:
    """
    :param diacritics: even though it's Modern Greek there can be still instances of polytonic texts
    :param diaeresis:   if dieresis is true, it checks if dieresis is expected because of accent position and puts it.
    :return:
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


remove_all_diacritics = remove_diacritics(PSILI, DASIA, OXIA, VARIA, PERISPOMENI, YPOGEGRAMMENI)

remove_all_diacritics_with_diaer = remove_diacritics(PSILI, DASIA, OXIA, VARIA, PERISPOMENI, YPOGEGRAMMENI, DIAERESIS)

remove_non_accent_diacritics = remove_diacritics(YPOGEGRAMMENI, ROUGH, SMOOTH)

remove_non_accent_diacritics_without_dierisis = remove_diacritics(YPOGEGRAMMENI, ROUGH, SMOOTH, diaeresis=False)

remove_diaer = remove_diacritics(DIAERESIS)


def convert_to_monotonic(sentence_or_word: str, one_syllable_rule: bool = True) -> str:
    sentence_or_word = remove_non_accent_diacritics_without_dierisis(sentence_or_word)
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
    :param syllable:
    :return: boolean, yes or no
    """
    for ch in unicodedata.normalize("NFD", syllable):
        if ch in [VARIA, OXIA, PERISPOMENI]:
            return True

    return False


def has_multiple_accents(word: str) -> bool:
    number_of_accents = 0
    for syllable in modern_greek_syllabify(word):
        if is_accented(syllable):
            number_of_accents += 1

        if number_of_accents > 1:
            return True

    return False


def put_accent_on_a_vowel(vowel: str) -> str:
    """
    :param vowel:
    :return: acute, if vowel with is accompanied by diaeresis, then diaeresis is left, all other accents are replaced by
    acute
    """
    vowel = remove_all_diacritics(vowel)
    if not vowel in vowels:
        return vowel

    return unicodedata.normalize("NFC", "".join((vowel, OXIA)))


def put_accent_on_syllable(syllable: str) -> str:
    """
    :param syllable:
    :return: accented syllable
    """
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


def where_is_accent(word: str, true_syllabification=True) -> str | None:
    """
    :param word:
    :param true_syllabification: that is where i before a vowel doesnt constitute a single syllable
    :return: ANTEPENULTIMATE, PENULTIMATE, ULTIMATE, 'incorrect_accent', and if there is no accent, None
    """

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


def put_accent(word: str, accent_name: str, true_syllabification=True) -> str:
    """
    :param word: can be already accented
    :param accent_name:ANTEPENULTIMATE, PENULTIMATE, ULTIMATE
    :param true_syllabification:
    :return: if accent_name param given incorrect, return input word
    """
    if accent_name == ULTIMATE:
        word = put_accent_on_the_ultimate(word, true_syllabification=true_syllabification)
    elif accent_name == PENULTIMATE:

        word = put_accent_on_the_penultimate(word, true_syllabification=true_syllabification)
    elif accent_name == ANTEPENULTIMATE:
        word = put_accent_on_the_antepenultimate(word, true_syllabification=true_syllabification)

    # check if there is a superflouus diaeresis in cases where ϊ (with diaeresis) is not an independent vowel ('ϊου' in eg 'ρολοϊου'),
    # and as a result we have syllabification of this kind: 'ρο-λο-ϊου'
    return word


def remove_redundand_diaeresis(word: str) -> str:
    redundant_diaereseis = {'όϊ': 'όι', 'άϊ': "άι", 'έϊ': "έι", 'ύϊ': 'ύι', 'όϋ': 'όυ'}
    if DIAERESIS in unicodedata.normalize('NFD', word):
        for redundant_diaeresis in redundant_diaereseis:
            if redundant_diaeresis in word:
                word = word.replace(redundant_diaeresis, redundant_diaereseis[redundant_diaeresis])
                break
    return word


def put_accent_on_the_ultimate(word: str, accent_one_syllable=True, second_accent=False, true_syllabification=True) -> str | None:
    # flag indicates if one syllable words should be accented

    if second_accent:
        if where_is_accent(
            word, true_syllabification=False
        ) == PENULTIMATE:
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


