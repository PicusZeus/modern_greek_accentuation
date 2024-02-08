from __future__ import annotations
from modern_greek_accentuation.accentuation import *
from modern_greek_accentuation.resources import *
from modern_greek_accentuation.syllabify import modern_greek_syllabify
from typing import List


def add_augment(not_augmented_form: str) -> set[str]:
    """
    :param not_augmented_form: past verb form without an augment or perfect participle.
    only for creating regular past tenses. deals with prefixes.
    :return: Augmented verb form or perfect participle. It also deals with reduplication.
     The result must be checked against a data base of existing
     words. accent on antepenultimate
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


def add_augment_with_prefix(prefixes: dict, not_augmented_form: str, on_vowel: bool = False):
    """

    :param prefixes:
    :param not_augmented_form:
    :param results:
    :param on_vowel:
    :return:
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


def deaugment_prefixed_stem(stem: str) -> str:
    """
    :param stem: verb stem with cut off ending, prefixed
    :return: check if the stem is augmented and if it is, returns an anaugmented stem without any accent
    """

    for pref in sorted(dict_of_augmented_prefixes.items(), key=lambda key: len(key[1]), reverse=True):
        if pref[1] == remove_all_diacritics(stem[:len(pref[1])]):

            prefix = pref[0].strip()
            verb = stem[len(pref[1]):]

            if prefix[-1] == 'ν':
                if verb[0] in ['γ', 'χ', 'κ', 'ξ']:
                    prefix = prefix[:-1] + 'γ'
                if verb[0] == 'λ':
                    prefix = prefix[:-1] + 'λ'
                if verb[0] in ['μ' 'φ', 'β', 'π', 'ψ']:
                    prefix = prefix[:-1] + 'μ'
                if verb[0] in ['σ', 'ζ']:
                    prefix = prefix[:-1]

            return prefix + verb

    return remove_all_diacritics(stem)


def deaugment_stem(stem: str, lemma: str) -> str | None:
    """
    :param stem: verb stem
    :param lemma: lemma is needed to check if an anaugmented stem begins on e or a
    :return: deaugmented_stem if successful, else None, it must be checked against a data base of all forms
    """

    if count_syllables(stem, true_syllabification=False) == 2 and stem[-1] != 'ι':
        if stem[0] in ['έ', 'ή']:
            deagmented_stem = stem[1:]
            if lemma[0] in ['ε', 'α', 'ά', 'έ'] and stem[0] in ['ή']:
                deagmented_stem = lemma[0] + deagmented_stem
            elif lemma[0] == 'ε':
                deagmented_stem = stem
            return deagmented_stem
    return None


def deaugment_past_form(form: str, lemma: str) -> str:
    """
    :param form: verb
    :param lemma: lemma is needed to check if an anaugmented stem begins on e or a
    :return: deaugmented_stem if successful, else None, it must be checked against a data base of all forms
    """

    if form[0] in ['έ', 'ή']:
        deagmented_stem = form[1:]
        if lemma[0] in ['ε', 'α', 'ά', 'έ'] and form[0] in ['ή']:
            deagmented_stem = lemma[0] + deagmented_stem
        elif lemma[0] == 'ε':
            deagmented_stem = form
        return deagmented_stem
    return form


def put_accent_on_past_tense(past_form: str, present_form: str) -> str:
    """
    :param past_form:  a result of adding an ending to a past stem
    :param present_form:
    :return: put an accent on antepenultimate and if necessary deals with an augment,
    that is it removes it if it's not accented
     this function is not applicable to paratatikos in second con.
     It returns also two error messages: "it's not a valid form", "it's not a valid verb form", if described situations
     take place
    """

    result = past_form

    prefix = ''
    # if there is a prefix that doesn't influence the verb form, cut it and attach at the end, so that
    # augments can be correctly handled

    for pref in prefixes_detachable:

        if pref == past_form[:len(pref)]:
            prefix = pref
            break

    result = remove_all_diacritics(result)

    syllables = modern_greek_syllabify(result)

    if len(syllables) > 3:

        # if there is unaccented augment, strip it
        # but be careful with e or h that are parts of the stem in the present
        if result[0] == 'ε' and present_form[0] != 'ε':
            result = prefix + result[1:]

        elif result[0] == 'η' and present_form[0] == 'ε':
            result = prefix + 'ε' + result[1:]

    else:
        result = prefix + result

    return put_accent_on_the_antepenultimate(result, true_syllabification=False)
