# Modern-greek-accentuation

Python 3 library for analyzing, accenting, syllabification, augmentation and transcription of Modern Greek Words

# Documentation

see [docs.rst](https://github.com/PicusZeus/modern_greek_accentuation/blob/master/docs.rst)


# Change Log

 * 0.2.3 Fixed issue with syllabification, where iota with diaeresis is not an independent vowel (ρολοϊού), also fixed
 a secondary issue with accentuation, where previously redundant diaeresis was not removed in above cases.
 * 0.2.2 Fixed issue with internal augmentation with unaccented augment, now it gives such an option
 * 0.2.1 Added transcription module (simple, Erasmian and modern for Polish readers)
 * 0.1.1 Initial release