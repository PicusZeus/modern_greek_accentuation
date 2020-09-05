from .syllabify import *
import unicodedata


def remove_diacritics(*diacritics, diaeresis=True):
    """
    :param diacritics: even though it's Modern Greek there can be still instances of polytonic texts
    :param diaeresis:   if dieresis is true, it checks if dieresis is expected because of accent position and puts it.
    :return:
    """
    def _(text, dieresis=diaeresis):
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

remove_diaer = remove_diacritics(DIAERESIS)


def is_accented(syllable):
    """
    :param syllable:
    :return: boolean, yes or no
    """
    for ch in unicodedata.normalize("NFD", syllable):
        if ch in [VARIA, OXIA, PERISPOMENI]:
            return True

    return False


def put_accent_on_a_vowel(vowel):
    """
    :param vowel:
    :return: acute, if vowel with is accompanied by diaeresis, then diaeresis is left, all other accents are replaced by
    acute
    """
    vowel = remove_all_diacritics(vowel)
    if not vowel in vowels:
        return vowel

    return unicodedata.normalize("NFC", "".join((vowel, OXIA)))


def put_accent_on_syllable(syllable):
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

    diaeresis_dipht = {'όϊ':'όι', 'άϊ': "άι", 'έϊ': "έι", 'ύϊ': 'ύι', 'όϋ': 'όυ'}

    # but if accent makes diaeresis redundant, it should be removed
    for diaer_with_acc in diaeresis_dipht.keys():
        if diaer_with_acc in accented_syllable:
            accented_syllable = accented_syllable.replace(diaer_with_acc, diaeresis_dipht[diaer_with_acc])

    return accented_syllable


def where_is_accent(word, true_syllabification=True):
    """
    :param word:
    :param true_syllabification: that is where i before a vowel doesnt constitute a single syllable
    :return: 'antepenultimate', 'penultimate', 'ultimate', 'incorrect_accent', and if there is no accent, None
    """
    which = None

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    syllables = reversed(syllables)
    for (index, syllable) in enumerate(syllables):
        if is_accented(syllable):
            which = index
            break
    if which == 0:
        return 'ultimate'
    elif which == 1:
        return 'penultimate'
    elif which == 2:
        return 'antepenultimate'
    elif not which:
        return None
    else:
        return 'incorrect_accent'


def put_accent(word, accent_name, true_syllabification=True):
    """

    :param word:
    :param accent_name:'antepenultimate', 'penultimate', 'ultimate'
    :param true_syllabification:
    :return: if accent_name param given incorrect, return input word
    """
    if accent_name == 'ultimate':
        word = put_accent_on_the_ultimate(word)
    elif accent_name == 'penultimate':


        word = put_accent_on_the_penultimate(word, true_syllabification=true_syllabification)
    elif accent_name == 'antepenultimate':
        word = put_accent_on_the_antepenultimate(word, true_syllabification=true_syllabification)

    return word





def put_accent_on_the_ultimate(word, accent_one_syllable=True, second_accent=False):
    # flag indicates if one syllable words should be accented

    if second_accent:
        if where_is_accent(
            word, true_syllabification=False
        ) == 'penultimate':
            pass
        else:

            word = remove_all_diacritics(word)
    else:
        word = remove_all_diacritics(word)

    syllables = modern_greek_syllabify(word)

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


def put_accent_on_the_penultimate(word, true_syllabification=True):
    # if one syllable, do not put any accent
    word = remove_all_diacritics(word)
    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    if len(syllables) > 1:
        to_be_accented = syllables[-2]
        accented = put_accent_on_syllable(to_be_accented)
       
        syllables[-2] = accented
        res = ''.join(syllables)
    
        return res
    else:
        return word


def put_accent_on_the_antepenultimate(word, true_syllabification=True):
    # if one syllable word given, doesnt put accent

    word = remove_all_diacritics(word)

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    # if word is accented on ult, antepenult is still possible
    if len(syllables) > 2:

        to_be_accented = syllables[-3]

        accented = put_accent_on_syllable(to_be_accented)

        syllables[-3] = accented
        res = ''.join(syllables)
        return res
    else:
        res = put_accent_on_the_penultimate(word)

    return res


