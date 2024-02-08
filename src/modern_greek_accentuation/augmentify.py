from __future__ import annotations
from modern_greek_accentuation.accentuation import *
from modern_greek_accentuation.resources import *
from modern_greek_accentuation.syllabify import modern_greek_syllabify
from typing import List


def add_augment(not_augmented_form: str) -> set[str]:
    """
    **This functions create quite often multiple "proposals" for an augmented form, since it is a semi regular process in Modern Greek.**

    :param not_augmented_form: Past verb form without an augment or perfect participle that needs to be augmented/reduplicated. Works also for internal augment.
    :return: A set with zero or more guessed forms.
    """
    results = []
    try:
        second_syllable = modern_greek_syllabify(not_augmented_form)[-2]
        sinizisi = count_syllables(second_syllable) != count_syllables(second_syllable, true_syllabification=False)
    except IndexError:
        sinizisi = False

    if count_syllables(not_augmented_form, False) > 2:
        results = [put_accent_on_the_antepenultimate(
            not_augmented_form, False)]
        if not sinizisi:
            results.append(not_augmented_form)
        if not sinizisi or count_syllables(not_augmented_form) > 2:
            results.append(put_accent_on_the_antepenultimate(not_augmented_form))

    results.extend(add_augment_with_prefix(prefixes_before_augment, not_augmented_form))

    results.extend(add_augment_with_prefix(prefixes_before_augment_on_vowel, not_augmented_form, on_vowel=True))
    if not_augmented_form.endswith('μένος'):
        results = [put_accent_on_the_penultimate(v) for v in results]

    return set(results)


def add_augment_with_prefix(prefixes: dict, not_augmented_form: str, on_vowel: bool = False) -> list[str]:
    """
    **Helper function to be used in the `add_augment` function**

    :param prefixes: a dictionary with prefixes as keys and prefixes before augment as values.
    :param not_augmented_form: A past form with only past ending, before augmentation.
    :param on_vowel: If on_vowel is False (default) it expects the (stem) verb to begin with a consonant.
    :return: a list with guessed forms.
    """
    result = []
    for pref in prefixes.keys():
        pref = pref.strip()
        verb = not_augmented_form[len(pref):]
        if on_vowel and verb and not verb[0] in vowels:
            continue
        sub_res = []
        reduplication = False
        if len(verb) > 1 and pref == remove_all_diacritics(not_augmented_form[:len(pref)]):
            if not verb.endswith('μένος') and not verb.endswith('το') and not verb.endswith('μην'):

                if verb[0] in ['ι', 'α', 'ε', 'ο', 'ά', 'έ', 'ό', 'ί']:
                    if verb[:2] in ['ευ', 'εύ', 'αυ', 'αύ']:

                        form = put_accent_on_the_antepenultimate('ηυ' + verb[2:])

                        sub_res.append(form)

                    elif verb[:2] in ['αι', 'αί', 'ει', 'εί']:
                        form = put_accent_on_the_antepenultimate('η' + verb[2:])
                        sub_res.append(form)

                    elif verb[0] in ['ε', 'έ']:
                        form = put_accent_on_the_antepenultimate('ει' + verb[1:])
                        sub_res.append(form)
                        form = put_accent_on_the_antepenultimate('η' + verb[1:])
                        sub_res.append(form)

                    elif verb[0] in ['α', 'ά']:
                        form = put_accent_on_the_antepenultimate('η' + verb[1:])
                        sub_res.append(form)

                    elif verb[0] in ['ε', 'έ', 'ι', 'ί']:
                        form = put_accent_on_the_antepenultimate('ει' + verb[1:])
                        sub_res.append(form)

                    elif verb[0] in ['ο' 'ό']:
                        form = put_accent_on_the_antepenultimate('ω' + verb[1:])
                        sub_res.append(form)

                elif verb.startswith('θέλ') or verb.startswith('ξέρ'):
                    form = put_accent_on_the_antepenultimate('η' + verb)
                    sub_res.append(form)
                elif count_syllables(verb) and verb[0] not in vowels:
                    form = put_accent_on_the_antepenultimate('ε' + verb)
                    sub_res.append(form)

            # archaic aorist

            if verb[-2:] in ['ην', 'ον'] or verb[-1] == 'η':

                if verb[0] in ['α', 'ά']:
                    form = 'η' + verb[1:]
                    sub_res.append(form)
                    if verb == 'άστη':
                        sub_res.append('έστη')

                elif verb[0] in ['ε', 'έ']:
                    form = 'ει' + verb[1:]
                    sub_res.append(form)
                    form = 'η' + verb[1:]
                    sub_res.append(form)
                elif verb[0] in ['ο' 'ό']:
                    form = 'ω' + verb[1:]
                    sub_res.append(form)
                elif verb[0] == 'ρ':
                    form = 'ερ' + verb
                    sub_res.append(form)
                else:
                    form = 'ε' + verb
                    sub_res.append(form)
                if verb[-2:] in ['ην'] or verb[-1] in ['η']:
                    sub_res = [put_accent_on_the_penultimate(f) for f in sub_res]
                else:
                    sub_res = [put_accent_on_the_antepenultimate(f) for f in sub_res]

            # archaic paratatikos without accent change
            elif verb[-2:] in ['το'] or verb[-3:] == 'μην':
                form = 'ε' + verb
                sub_res.append(form)
                sub_res.append(verb)

            # perfect participle
            elif verb.endswith('μένος'):
                # if on_vowel:
                #     sub_res.append(verb)
                reduplication = False

                if verb[0] not in vowels and verb[0] not in ['ψ', 'ξ'] and verb[1] in [*vowels, 'ρ', 'λ']:
                    reduplication = True
                    # reduplication
                    # form = verb[0] + 'ε' + verb
                    if verb[0] == 'θ':
                        form = 'τε' + verb
                    elif verb[0] == 'χ':
                        form = 'κε' + verb
                    elif verb[0] == 'ρ':
                        form = 'ερ' + verb
                    else:
                        form = verb[0] + 'ε' + verb

                    sub_res.append(form)

                    # augmentation
                elif verb[:2] in ['ευ', 'εύ', 'αυ', 'αύ']:
                    sub_res.append('ηυ' + verb[2:])
                elif verb[0] not in vowels or verb[0] in ['ξ', 'ψ']:
                    form = 'ε' + verb
                    sub_res.append(form)

            if reduplication:
                # because when reduplicating prefix (like συγ) should stay the same
                sub_res = [pref + augmented for augmented in sub_res]
            else:
                sub_res = [prefixes[pref] + augmented for augmented in sub_res]

            result.extend(sub_res)

        # filter_out irregularities
    results = list(set(result))
    # results = [f for f in results if
    #            count_syllables(f, true_syllabification=False) > 2 or f[:-1] in ['πήγ', 'πήρ', 'είχ', 'ήρθ',
    #                                                                             'ήλθ', 'βρήκ', 'μπήκ', 'βηήκ',
    #                                                                             'βήκ', 'είπ', 'είδ', 'ήπι',
    #                                                                             'ήρ',
    #                                                                             'ήχθ', 'ήγ']]
    return results


def deaugment_stem(stem: str, lemma: str) -> str | None:
    """
    **A function can be useful if you want to conjugate in the past tense a Greek verb that has an augment**

    :param stem: a non prefixed verb past stem (without endings) that is or is supposed to be augmented, so it must has two syllable (like έκαν from έκανα)
    :param lemma: Present form, and so unaugmented, of a verb.
    :return: deaugmented (if augment wasn't accented in the first place) verb stem without accent, if not able to create, return None
    """

    if count_syllables(stem, true_syllabification=False) == 2 and stem[-1] != 'ι':
        if stem[0] in ['έ', 'ή']:
            deagmented_stem = stem[1:]
            if lemma[0] in ['ε', 'α', 'ά', 'έ'] and stem[0] in ['ή']:
                deagmented_stem = lemma[0] + deagmented_stem
            elif lemma[0] == 'ε':
                deagmented_stem = stem
            return remove_all_accents(deagmented_stem)
    return None


def deaugment_prefixed_form(stem: str) -> str:
    """
    :param stem: a verb stem (without an ending) that is or is supposed to be internally augmented
    :return: a prefixed verb stem with augment removed only if it was accented
    """

    for pref in sorted(dict_of_augmented_prefixes.items(), key=lambda key: len(key[1]), reverse=True):
        if pref[1] == remove_all_diacritics(stem[:len(pref[1])]):

            prefix = pref[0].strip()
            verb = stem[len(pref[1]):]
            if count_syllables(verb, False) > 1:
                # we don't want to remove augment if the augment wasnt accented in the first place
                return remove_all_accents(stem)

            elif prefix[-1] == 'ν':
                if verb[0] in ['γ', 'χ', 'κ', 'ξ']:
                    prefix = prefix[:-1] + 'γ'
                if verb[0] == 'λ':
                    prefix = prefix[:-1] + 'λ'
                if verb[0] in ['μ' 'φ', 'β', 'π', 'ψ']:
                    prefix = prefix[:-1] + 'μ'
                if verb[0] in ['σ', 'ζ']:
                    prefix = prefix[:-1]

            return remove_all_accents(prefix + verb)

    return remove_all_accents(stem)


def deaugment_past_form(form: str, lemma: str) -> str:
    """
    :param form: an augmented past form, not prefixed
    :param lemma: lemma is needed to check if an unaugmented stem begins on e or a
    :return: deaugmented form if successful, else the given form, with removed accents
    """

    if form[0] in ['έ', 'ή']:
        deagmented_stem = form[1:]
        if lemma[0] in ['ε', 'α', 'ά', 'έ'] and form[0] in ['ή']:
            deagmented_stem = lemma[0] + deagmented_stem
        elif lemma[0] == 'ε':
            deagmented_stem = form
        return remove_all_accents(deagmented_stem)
    return remove_all_accents(form)
