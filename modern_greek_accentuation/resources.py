
PSILI = SMOOTH = "\u0313"
DASIA = ROUGH = "\u0314"
OXIA = ACUTE = "\u0301"
VARIA = GRAVE = "\u0300"
PERISPOMENI = CIRCUMFLEX = "\u0342"
YPOGEGRAMMENI = IOTA_SUBSCRIPT = "\u0345"
DIAERESIS = "\u0308"

ANTEPENULTIMATE = 'antepenultimate'
PENULTIMATE = 'penultimate'
ULTIMATE = 'ultimate'


vowels_dict = {'ά': 'α', 'έ': 'ε', 'ί': 'ι', 'ύ': 'υ', 'ό': 'ο', 'ώ': 'ω', 'ή': 'η', 'ΐ': 'ϊ', 'ΰ': 'ϋ'}

vowels_accented = ['ά', 'έ', 'ί', 'ύ', 'ό', 'ώ', 'ή', 'ΐ', 'ΰ']

vowels_unaccented = ['α', 'ε', 'ι', 'υ', 'ο', 'ω', 'η', 'ϊ', 'ϋ']

vowels = ['ά', 'α', 'έ', 'ε', 'ί', 'ι', 'ύ', 'υ', 'ό','ο', 'ώ', 'ω', 'ή', 'η','ΐ', 'ϊ', 'ΰ', 'ϋ']

un_single_i = ['ι', 'η', 'υ', 'ϊ']

un_digraph_i = ['οι', 'ει', 'υι']

valid_cons_cluster = ['στ', 'χρ', 'μπ', 'ντ', 'χτ', 'χθ', 'γδ']

diphtongs_dict = {'αύ': 'αυ', 'εύ': 'ευ', 'εί': 'ει', 'οί': 'οι', 'υί': 'υι', 'ού': 'ου', 'άη': 'αη', 'όη': 'οη', 'άι': 'αϊ', 'όι': 'οϊ', 'αί': 'αι'}

diphtongs = ['αύ', 'αυ', 'εύ', 'ευ', 'εί', 'ει', 'οί', 'οι', 'υί','υι', 'ού', 'ου', 'άη', 'αη', 'όη', 'οη',
             'άι', 'αϊ', 'όι', 'οϊ', 'αί', 'αι']



vowels_anc_transcription = {'α': 'a', 'ε': 'e', 'ι': 'i', 'υ': 'y', 'ο': 'o', 'ω': 'o',
                            'η': 'h', 'ϊ': 'i', 'ϋ': 'u'}

vowels_mod_transcription = {'α': 'a', 'ε': 'e', 'ι': 'i', 'υ': 'i', 'ο': 'o', 'ω': 'o', 'η': 'i',
                            'ϊ': 'i', 'ϋ': 'i'}

consonants_anc_transcription = {'β': 'b', 'γ': 'g', 'δ': 'd', 'θ':'th', 'ζ': 'z', 'λ':'l', 'κ':'k',
                                'μ':'m', 'ν':'n', 'π':'p', 'ρ':'r', 'σ':'s', 'ς':'s', 'τ':'t', 'φ':'f',
                                'ψ':'ps', 'ξ':'ks'}

consonants_mod_transcription = {'β': 'w', 'γ': 'gh', 'δ': 'dh', 'θ':'th', 'λ':'l', 'μ':'m', 'ν':'n',
                                'π':'p', 'ρ':'r', 'σ':'s', 'ς':'s', 'τ':'t', 'φ':'f', 'ψ':'ps', 'ξ':'ks', 'χ': 'ch'}

digraphs_anc_transcirption = {'αυ': 'au', 'ευ': 'eu', 'γγ': 'ng', 'γκ': 'nk', 'γχ': 'nch', 'ου': 'ou'}

digraphs_mod_transciption = {'αυ': 'aw', 'ευ': 'ew', 'γγ': 'ng', 'γκ': 'ng', 'γχ': 'nch',
                             'ου': 'u', 'αι': 'e', 'οι': 'i', 'ει': 'i', 'υι': 'i', 'ηυ': 'iw'}


ancient_tr = {'vowels': vowels_anc_transcription,
              'consonants': consonants_anc_transcription,
              'digraphs': digraphs_anc_transcirption}

modern_tr = {'vowels': vowels_mod_transcription,
             'consonants': consonants_mod_transcription,
             'digraphs': digraphs_mod_transciption}

list_of_def_diphthongs = ['ειευ', 'οιευ', 'ιευ', 'ειαυ', 'οιαυ', 'ιαυ', 'ιου', 'οιου', 'ειου', 'υου', 'οια', 'οιε',
                          'οιι', 'οιυ', 'οιο', 'οιω', 'οιη', 'εια', 'ειε', 'ειι', 'ειυ', 'ειο', 'ειω', 'ειη', 'υια',
                          'υιε', 'υιι', 'υιυ', 'υιο', 'υιω', 'υιη', 'ια', 'ιε', 'ιι', 'ιυ', 'ιο', 'ιω', 'ιη', 'ηα',
                          'ηε', 'ηι', 'ηυ', 'ηο', 'ηω', 'ηη', 'ηϊ', 'ηϋ', 'υα', 'υε', 'υι', 'υυ', 'υο', 'υω', 'υη']


# these prefixes change themselves or stem by esoteric augmentation
# I probably should change this model into key - augmented prefix, value -
# unaugmented, because for one augmented there are sometimes more than one
# unaugmented forms (para: pare, or parh)
dict_of_augmented_prefixes = {'ανα': 'ανε', 'δια': 'διε', 'εκ': 'εξε', 'συλ': 'συνε', 'απο': 'απε', 'προ': 'προε',
                              'κατευ': 'κατηυ', 'παρα': 'παρη', 'παρα ': 'παρε', 'προεξ': 'προεξε', 'ενδια': 'ενδιε',
                              'περι': 'περιε', 'υπα': 'υπη',
                              'υπο': 'υπε', 'αμφι': 'αμφε', 'επιπαρα ': 'παρεεπε', 'κατα':'κατε', 'εισ': 'εισε', 'συμ': 'συνε',
                              'συγ': 'συνε', 'συ': 'συνε', 'ελ': 'εξε'}

# these prefixes do not merge with verbs at all - there are more, add them in the future
prefixes_list_that_allow_augmentaion = ['πολυ', 'παρα', 'καλα', 'κουτσο', 'ξανα']

# for automatic augmentation of regular stems
prefixes_before_augment = {'ανα': 'αν', 'διακατ': 'διακατ', 'αν': 'αν', 'δια': 'δι', 'δι': 'δι', 'εκ': 'εξ',
                           'συλ': 'συν', 'εμπερι': 'εμπερι', 'επανεξ': 'επανεξ',
'απο': 'απ', 'κακο': 'κακο', 'καλο':'καλο',
                            'απ': 'απ', 'προ': 'προ', 'κατα': 'κατ', 'κατ': 'κατ', 'παρα': 'παρα', ' παρα':'παρ',
                           'παρ': 'παρ', 'προσ': 'προσ', 'μετα': 'μετ', ' μετ': 'μετ',
                            'προεκ': 'προεξ', 'ενδια': 'ενδι', 'ενδι': 'ενδι', 'περι': 'περι', 'υπο': 'υπ',
                           'υπ': 'υπ', 'αμφι': 'αμφ', 'επι': 'επ', 'επ': 'επ', 'εισ': 'εισ', 'συμ': 'συν',
                            'συγ': 'συν', 'συ': 'συν', 'συν': 'συν', 'ελ': 'εξ','πολυ': 'πολυ',
                           'επεμ': 'επεν', 'υπερ': 'υπερ', 'προεξ': 'προεξ', 'αυτοκατα': 'αυτοκατ', 'συγκατα':'συγκατ',
                           'επεν': 'επεν', 'επεγ': 'επεν', 'παρεμ': 'παρεν', 'παρεν':'παρεν', 'παρεγ':'παρεν',
                           'εν': 'εν', 'εμ': 'εν', 'εγ': 'εν', 'εγκατα': 'εγκατ', 'υφ': 'υφ',
                           'καλα': 'καλα', 'κουτσο': 'κουτσο', 'ξανα': 'ξανα', 'εξ':'εξ', 'συμμετ':'συμμετ',
                           'ξε':'ξε', ' ξε': 'ξ', 'επανα': 'επαν', 'επαν': 'επαν', 'αντι': 'αντ', 'αντ': 'αντ',
                           '': ''}
                           


