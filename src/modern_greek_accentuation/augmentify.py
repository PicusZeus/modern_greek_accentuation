from .accentuation import *
from .resources import *


def add_augment(not_augmented_form):
    """
    :param not_augmented_form: past verb form without an augment or perfect participle.
    only for creating regular past tenses. deals with prefixes.
    :return: Augmented verb form or perfect participle. It also deals with reduplication.
     The result must be checked against a data base of existing
     words. accent on antepenultimate
    """

    results = [put_accent_on_the_antepenultimate(not_augmented_form), put_accent_on_the_antepenultimate(
        not_augmented_form, False), not_augmented_form]
    for pref in prefixes_before_augment.keys():

        if pref.strip() == remove_all_diacritics(not_augmented_form[:len(pref.strip())]):

            verb = not_augmented_form[len(pref.strip()):]
            sub_res = [put_accent_on_the_antepenultimate(verb)]

            if count_syllables(verb) in [2, 3] and verb[0] in ['α', 'ε', 'ο', 'ά', 'έ', 'ό']:
                if verb[0] in ['ε', 'α', 'έ', 'ά']:
                    form = put_accent_on_the_antepenultimate('η' + verb[1:])
                    sub_res.append(form)
                if verb[0] in ['ε', 'έ']:
                    form = put_accent_on_the_antepenultimate('ει' + verb[1:])
                    sub_res.append(form)
                if verb[0] in ['ο' 'ό']:
                    form = put_accent_on_the_antepenultimate('ω' + verb[1:])
                    sub_res.append(form)
            elif verb[-1] in ['α', 'ε']:
                form = put_accent_on_the_antepenultimate('ε' + verb)
                if verb[:-1] in ['θέλ', 'ξέρ']:
                    form = put_accent_on_the_antepenultimate('η' + verb)
                sub_res.append(form)

            # archaic aorist

            elif verb[-2:] in ['ην', 'ον'] or verb[-1] == 'η':
                if verb[0] in ['α', 'ά']:
                    form = 'η' + verb[1:]
                    sub_res.append(form)
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
                if verb[-2:] in ['ην'] or verb[-1] == 'η':
                    sub_res = [put_accent_on_the_penultimate(f) for f in sub_res]
                else:
                    sub_res = [put_accent_on_the_antepenultimate(f) for f in sub_res]

            # archaic paratatikos without accent change
            elif verb[-2:] in ['το'] or verb[-3:] == 'μην':
                form = 'ε' + verb
                sub_res.append(form)
                sub_res.append(verb)

            # perfect participle
            elif verb[-2:] == 'ος':
                sub_res.append(verb)
                if verb[0] not in vowels:
                    # reduplication
                    form = verb[0] + 'ε' + verb
                    sub_res.append(form)
                    # augmentation
                    form = 'ε' + verb
                    sub_res.append(form)

            sub_res = [prefixes_before_augment[pref] + augmented for augmented in sub_res]

            results.extend(sub_res)

            # filter_out irregularities
            results = list(set(results))
            results = [f for f in results if count_syllables(f) > 2 or f[:-1] in ['πήγ', 'πήρ', 'είχ', 'ήρθ',
                                                                                 'ήλθ', 'βρήκ', 'μπήκ', 'βηήκ',
                                                                                 'βήκ', 'είπ', 'είδ', 'ήπι']]

    return results


def deaugment_prefixed_stem(stem):
    """
    :param stem: verb stem with cut off ending, prefixed
    :return: check if the stem is augmented and if it is, returns an anaugmented stem
    """

    for pref in dict_of_augmented_prefixes.items():

        if len(stem) > len(pref[1]) and pref[1] == stem[:len(pref[1])]:
            return pref[0].strip() + stem[len(pref[1]):]

    return stem


def deaugment_stem(stem, lemma):
    """
    :param stem: verb stem
    :param lemma: lemma is needed to check if an anaugmented stem begins on e or a
    :return: deaugmented_stem if successful, else None, it must be checked against a data base of all forms
    """

    if count_syllables(stem, true_syllabification=False) == 2 and stem[-1] != 'ι':
        if stem[0] in ['έ', 'ή']:
            deagmented_stem = stem[1:]
            if lemma[0] in ['ε', 'α'] and stem[0] in ['ή']:
                deagmented_stem = lemma[0] + deagmented_stem
            return deagmented_stem
    return None


def put_accent_on_past_tense(past_form, present_form):
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
    for pref in prefixes_list_that_allow_augmentaion:

        if pref == past_form[:len(pref)]:
            prefix = pref
            present_form = present_form[len(pref):]
            result = past_form[len(pref):]

    result = remove_all_diacritics(result)

    syllables = modern_greek_syllabify(result)

    if len(syllables) > 3:

        # if there is unaccented augment, strip it
        # but be careful with e or h that are parts of the stem in the present
        if result[0] == 'ε' and present_form[0] != 'ε':
            result = result[1:]

        if result[0] == 'η' and present_form[0] == 'ε':
            result = 'ε' + result[1:]

        syllables = modern_greek_syllabify(result)

    if len(syllables) >= 3:
        to_be_accented = syllables[-3]
        accented = put_accent_on_syllable(to_be_accented)
        if not accented:
            return "it's not a valid form"
        syllables[-3] = accented
    else:
        try:
            to_be_accented = syllables[-2]
            accented = put_accent_on_syllable(to_be_accented)
        except:
            return "it's not a valid verb form"

        syllables[-2] = accented

    result = ''.join(syllables)

    return prefix + result


