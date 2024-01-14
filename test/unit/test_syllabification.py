from unittest import TestCase
from modern_greek_accentuation import syllabify
# from icecream import ic


class Syllabification(TestCase):

    def test_simple_syllabification(self):
        r = syllabify.modern_greek_syllabify('άνθρωπος')
        r1 = syllabify.modern_greek_syllabify('ΆΝΘΡΩΠΟΣ')
        self.assertListEqual(['άν', 'θρω', 'πος'], r)
        self.assertListEqual(['ΆΝ', 'ΘΡΩ', 'ΠΟΣ'], r1)

    def test_true_syllabification(self):
        r1 = syllabify.modern_greek_syllabify('ρολοϊού')
        r2 = syllabify.modern_greek_syllabify("ρολογιού")
        r3 = syllabify.modern_greek_syllabify('ρολοϊου')
        r4 = syllabify.modern_greek_syllabify('κύριου')
        r5 = syllabify.modern_greek_syllabify('κυριου', true_syllabification=False)
        r6 = syllabify.modern_greek_syllabify('Υιός', true_syllabification=False)

        self.assertListEqual(['ρο', 'λο', 'ϊού'], r1)
        self.assertListEqual(['ρο', 'λο', 'γιού'], r2)
        self.assertListEqual(['ρο', 'λο', 'ϊου'], r3)
        self.assertListEqual(['κύ', 'ριου'], r4)
        self.assertListEqual(['κυ', 'ρι', 'ου'], r5)
        self.assertListEqual(['Υι', 'ός'], r6)
