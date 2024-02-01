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
        r7 = syllabify.modern_greek_syllabify('κήπος')
        r8 = syllabify.modern_greek_syllabify('αέρας')
        r9 = syllabify.modern_greek_syllabify('αγάπη')
        r10 = syllabify.modern_greek_syllabify('φεγγάρι')
        r11 = syllabify.modern_greek_syllabify('πατρίδα')
        r12 = syllabify.modern_greek_syllabify('γιορτή')
        r13 = syllabify.modern_greek_syllabify('εχθρός')
        r14 = syllabify.modern_greek_syllabify('άνθρωπος')
        r15 = syllabify.modern_greek_syllabify('καμπάνα')
        r16 = syllabify.modern_greek_syllabify('αγκινάρα')
        r17 = syllabify.modern_greek_syllabify('κατσίκα')
        r18 = syllabify.modern_greek_syllabify('μαύρο')
        r19 = syllabify.modern_greek_syllabify('αηδόνι')
        r20 = syllabify.modern_greek_syllabify('δουλειά')
        r21 = syllabify.modern_greek_syllabify('μαγκώνω')


        self.assertListEqual(['ρο', 'λο', 'ϊού'], r1)
        self.assertListEqual(['ρο', 'λο', 'γιού'], r2)
        self.assertListEqual(['ρο', 'λο', 'ϊου'], r3)
        self.assertListEqual(['κύ', 'ριου'], r4)
        self.assertListEqual(['κυ', 'ρι', 'ου'], r5)
        self.assertListEqual(['Υι', 'ός'], r6)
        self.assertListEqual(['κή', 'πος'], r7)
        self.assertListEqual(['α', 'έ', 'ρας'], r8)
        self.assertListEqual(['α', 'γά', 'πη'], r9)
        self.assertListEqual(['φεγ', 'γά', 'ρι'], r10)
        self.assertListEqual(['πα', 'τρί', 'δα'], r11)
        self.assertListEqual(['γιορ', 'τή'], r12)
        self.assertListEqual(['ε', 'χθρός'], r13)
        self.assertListEqual(['άν', 'θρω', 'πος'], r14)
        self.assertListEqual(['κα', 'μπά', 'να'], r15)
        self.assertListEqual(['α', 'γκι', 'νά', 'ρα'], r16)
        self.assertListEqual(['κα', 'τσί', 'κα'], r17)
        self.assertListEqual(['μαύ', 'ρο'], r18)
        self.assertListEqual(['αη', 'δό', 'νι'], r19)
        self.assertListEqual(['δου', 'λειά'], r20)
        self.assertListEqual(['μα', 'γκώ', 'νω'], r21)