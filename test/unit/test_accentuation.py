from unittest import TestCase
from src import accentuation
from src.resources import ANTEPENULTIMATE, PENULTIMATE, ULTIMATE


class RemoveAccent(TestCase):
    def test_remove_acute(self):
        r = accentuation.remove_all_diacritics('άνθρωπος')
        self.assertEqual('ανθρωπος', r)

    def test_remove_without_diaeresis(self):
        r = accentuation.remove_all_diacritics('προϋπηρεσία')
        self.assertEqual('προϋπηρεσια', r)

    def test_remove_polytonic(self):
        r = accentuation.remove_all_diacritics('ἀγαθοῦ')
        self.assertEqual('αγαθου', r)

    def test_remove_with_diaeresis(self):
        r = accentuation.remove_all_diacritics_with_diaer('προϋπηρεσία')
        self.assertEqual('προυπηρεσια', r)

    def test_remove_only_diaeresis(self):
        r = accentuation.remove_diaer("προϋπηρεσία")
        self.assertEqual("προυπηρεσία", r)


class CheckAccentuation(TestCase):
    def test_check_is_accented_monotonic(self):
        r = accentuation.is_accented("πρό")
        self.assertTrue(r)

    def test_check_is_accented_polytonic(self):
        r = accentuation.is_accented("τοῦ")
        self.assertTrue(r)

    def test_where_is_accent_antepunultimate(self):
        r = accentuation.where_is_accent("άνθρωπος")
        self.assertEqual(ANTEPENULTIMATE, r)


    def test_where_is_accent_penultimate(self):
        r = accentuation.where_is_accent('γυναίκα')
        self.assertEqual(PENULTIMATE, r)

    def test_where_is_accent_ultimate(self):
        r = accentuation.where_is_accent('παιδί')
        self.assertEqual(ULTIMATE, r)

    def test_where_is_accent_true_syllabification_flag(self):
        r1 = accentuation.where_is_accent('κάποιας', true_syllabification=False)
        r2 = accentuation.where_is_accent('κάποιας', true_syllabification=True)
        self.assertEqual(r1, ANTEPENULTIMATE)
        self.assertEqual(r2, PENULTIMATE)


class PutAccent(TestCase):

    def test_put_accent_antepenultimate(self):
        r = accentuation.put_accent('ανθρωπος', ANTEPENULTIMATE)
        self.assertEqual('άνθρωπος', r)

    def test_put_accent_penultimate(self):
        r1 = accentuation.put_accent("γυναικα", PENULTIMATE)
        r2 = accentuation.put_accent("Βαϊου", PENULTIMATE)
        r3 = accentuation.put_accent("Βαϊου", PENULTIMATE, true_syllabification=False)
        r4 = accentuation.put_accent("διαβατηριου", PENULTIMATE, true_syllabification=False)
        self.assertEqual("γυναίκα", r1)
        self.assertEqual("Βάιου", r2)
        self.assertEqual("Βαΐου", r3)
        self.assertEqual("διαβατηρίου", r4)

    def put_accent_ultimate(self):
        r = accentuation.put_accent("παιδι", ULTIMATE)
        self.assertEqual("παιδί", r)

    def test_convert_to_monotonic(self):
        r = accentuation.convert_to_monotonic("ἐν τῷ πρόσθεν λόγῳ δεδήλωται.")
        self.assertEqual('εν τω πρόσθεν λόγω δεδήλωται.', r)
