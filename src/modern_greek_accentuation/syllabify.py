from modern_greek_accentuation.resources import *
from typing import List


def _cut_off_syllable(word: str, true_syllabification=False) -> tuple:
    """
    it is more complicated than it should be, but modern Greek rules on accentuation are somewhat convoluted
    :param word:
    :param true_syllabification: if true i before vowels treated as consonants
    :return: returns tuple syllable and rest of the word
    """

    all_letters = list(word)
    all_letters.reverse()

    for index, letter in enumerate(all_letters):

        if letter.lower() in vowels:
            border = index
            # if there is sth else
            if len(all_letters[border:]) > 1:

                # check for diphtongs
                # problem with diph αη in κάηκα
                if all_letters[border + 1] + letter in diphtongs and true_syllabification:
                    border += 1
                # elif all_letters[border + 1] + letter in allowed_clusters:
                #     border += 1
                elif all_letters[border + 1] + letter in [d for d in diphtongs if d not in ['αη', 'οη', 'άη', 'όη',
                                                                                            'άι', 'αϊ', 'όι', 'οϊ'
                                                                                            ]] and not \
                        true_syllabification:

                    border += 1
                # check if sth else
                if len(all_letters[border + 1:]) > 0:
                    # check for diphtongs with i
                    if true_syllabification:
                        # check if this i is a part of a digraph
                        if len(all_letters[border + 1:]) > 1 and all_letters[border + 2] + \
                                all_letters[border + 1] in un_digraph_i:
                            # is oi, ei....
                            border += 2
                        # check if single i

                        elif all_letters[border + 1] in un_single_i and len(all_letters[border + 1:]) > 1 and \
                                (all_letters[border + 2] + all_letters[border + 1]) not in ['ευ', 'εύ', 'αυ', 'αύ']:

                            border += 1

                    rest = all_letters[border + 1:]
                    cons = ''
                    for let in rest:
                        # if consonant shift border one step
                        if let not in vowels:
                            cons = let + cons
                            border += 1
                        else:
                            # but if there are more then one consonant, than check
                            # if the consonant cluster can be a start for a greek word

                            if len(cons) > 1 and cons[:2] in valid_cons_cluster:
                                difference = 0
                                border -= difference

                            elif len(cons) > 1:
                                border -= 1
                            # border one step back

                            result = all_letters[border + 1:]
                            result.reverse()
                            result = ''.join(result)

                            syllable = all_letters[:border + 1]
                            syllable.reverse()
                            syllable = ''.join(syllable)
                            return result, syllable

    if has_vowel(word):
        syllable = word
        return None, syllable

    # if only consonant given
    return word, None


def _divide_into_syllables(word: str, syllables: list = None, true_syllabification=False) -> tuple:
    # helping function, returns word chopped into syllables in reverse order,
    # if true_syllabification off, it takes into consideration unaccented 'i'.

    rest, syllable = _cut_off_syllable(word, true_syllabification=true_syllabification)

    if syllable:
        syllables.append(syllable)

    if rest and len(syllables) > 0:

        rest, syllables = _divide_into_syllables(rest, syllables, true_syllabification=true_syllabification)
    elif rest and len(syllables) == 0:
        # for verbs where root consists of a single consonant
        syllables.append(rest)

        return None, syllables

    return rest, syllables


def modern_greek_syllabify(word: str, true_syllabification: bool = True) -> List[str]:
    """
    There is a problem as to how treat 'i' before vowels, as it is inconsistent across Modern Greek
    (χρη-σι-μο-ποι-ώ, υ-γι-ής, κα-τα-πιώ, και-νού-ργιο, Γιε-ώ-ργι-ος κτλ.), which mainly comes from the injection of
    katarevousians words into dimotic vocabulary. It's impossible to know it without a db of all "logies lekseis".
    For the sake of accentuation, you can use true_syllabification flag, which if False, will divide words treating
    'i' always as vowel. Still the result of this function should be most of the time correct
    :param word: word in Greek chars, works best if the word is accented
    :param true_syllabification: if you want to divide word treating 'i' always as vowel, give it a False value
    :return: Array with syllables
    """

    rest, syllables = _divide_into_syllables(word, [], true_syllabification=true_syllabification)
    syllables.reverse()

    return syllables


def has_vowel(word: str) -> bool:
    for letter in word:
        if letter.lower() in vowels:
            return True
    return False


def is_vowel(letter: str) -> bool:
    if letter.lower() in vowels:
        return True
    return False


def count_syllables(word: str, true_syllabification: bool = True) -> int:
    # modern greek only

    syllables = modern_greek_syllabify(word, true_syllabification=true_syllabification)

    length = len(syllables)
    return length
