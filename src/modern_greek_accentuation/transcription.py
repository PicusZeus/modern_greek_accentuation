
import re
from .accentuation import remove_all_diacritics
from .syllabify import modern_greek_syllabify
from .resources import vowels, ancient_tr, modern_tr, ROUGH
import unicodedata

"""
TO DO: add transcription to greeklish
"""


def simple_transcription(word, h=None, modern=False):
    """
    This is the simplest possible transcription mostly based on Erasmian pronunciation. Such a transcription
    can be used for identifying words written with orthographic errors or written with latin chars.
    :param word: word written with Greek chars.
    :param h: you can define how to render 'η', default is 'h'.
    :param modern_tr: modern transcription method if True
    :return: transcription, returns capitalised or all upper or all lower depending on the input.
    """

    syllabified = modern_greek_syllabify(word, true_syllabification=False)

    transcr_meth = ancient_tr
    if modern:
        transcr_meth = modern_tr

    transcribed_syllables = []

    for syllable in syllabified:
        syllable = remove_all_diacritics(syllable)
        transcribed_syllable = ''
        while True:
            if syllable[:2].lower() in transcr_meth['digraphs'].keys():
                transcription = transcr_meth['digraphs'][syllable[:2].lower()]
                transcribed_syllable += transcription
                syllable = syllable[2:]
            elif syllable[0].lower() in transcr_meth['vowels'].keys():
                transcription = transcr_meth['vowels'][syllable[0].lower()]

                transcribed_syllable += transcription
                if h:
                    transcribed_syllable = transcribed_syllable.replace('h', h)

                syllable = syllable[1:]
            elif syllable[0].lower() in transcr_meth['consonants'].keys():
                transcription = transcr_meth['consonants'][syllable[0].lower()]
                transcribed_syllable += transcription
                syllable = syllable[1:]
            else:
                transcribed_syllable += syllable[0]
                syllable = syllable[1:]

            if len(syllable) == 0:
                if modern:

                    for ke, replacement in {'ke': 'kie', 'che': 'chie', 'ghe': 'ghie'}.items():
                        transcribed_syllable = transcribed_syllable.replace(ke, replacement)
                    transcribed_syllable = transcribed_syllable.replace('ghi', 'j')

                    if 'j' in transcribed_syllable and not set(list(transcribed_syllable)).intersection({'e', 'o', 'a', 'u', 'i'}):
                        transcribed_syllable = transcribed_syllable.replace('j', 'ji')
                break

        transcribed_syllables.append(transcribed_syllable)

    transcribed_word = ''.join(transcribed_syllables)

    transcribed_word = capitalize_or_upper_transcription(word, transcribed_word)

    return transcribed_word


def capitalize_or_upper_transcription(word, transcription):
    if word.capitalize() == word:
        transcribed_word = transcription.capitalize()
    elif word.isupper():
        transcribed_word = transcription.upper()
    else:
        return transcription
    return transcribed_word


def has_rough_breathing(word):
    decomposed = unicodedata.normalize("NFD", word[0])

    if decomposed[0].lower() in vowels:
        if ROUGH in decomposed:
            return True
        elif len(word) > 1:
            decomposed_2 = unicodedata.normalize('NFD', word[1])
            if ROUGH in decomposed_2 and decomposed_2 in vowels:
                return True
    return False


def erasmian_transcription(word):
    """
    It's basically ``simple_transcription`` but it renders rough breathing as 'h'
    :param word: word written in greek
    :return: Erasmian transcription
    """

    transcription = simple_transcription(word, h='e')
    if has_rough_breathing(word):
        transcription = 'h' + transcription
    transcription = capitalize_or_upper_transcription(word, transcription)
    return transcription


def modern_transcription(word):
    """
    It has nothing to do with phonetic transcription in international phonetic alphabet. It's thought only for Polish
    readers as a simple way to get transcription of Modern Greek texts accessible to lay people
    :param word: written in Greek chars
    :return: simple transcription in following Modern Greek pronunciation.
    """
    transcription = simple_transcription(word, modern=True)

    if 'w' in transcription:
        ws = re.finditer('w', transcription)
        for w in ws:
            index = w.start()
            if len(transcription) > index:

                if transcription[index+1] in ['t', 'p', 'k', 's'] or len(transcription) > index + 3 and transcription[index+1:index+3] == 'ch':
                    transcription = transcription[:index] + 'f' + transcription[index+1:]

            else:
                transcription[index] = 'f'
    return transcription


