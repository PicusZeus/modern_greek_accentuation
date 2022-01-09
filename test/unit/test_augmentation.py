from unittest import TestCase
from src import augmentify


class Augmentation(TestCase):

    def test_hthela(self):
        al = list(augmentify.add_augment('θέλα'))
        self.assertIn('ήθελα', al)

    def test_upofera(self):
        al = list(augmentify.add_augment('υποφερα'))
        self.assertIn('υπέφερα', al)

    def test_prokeitai(self):
        al = list(augmentify.add_augment('πρόκειτο'))
        self.assertIn('επρόκειτο', al)

    def test_dedomenos(self):
        al = list(augmentify.add_augment('δομένος'))
        self.assertIn('δεδομένος', al)

    def test_sunelambana(self):
        al = list(augmentify.add_augment('συλλάμβανα'))
        self.assertIn('συνελάμβανα', al)


class PutAccentAndAugmentify(TestCase):

    def test_put_accent_ekane(self):
        r = augmentify.put_accent_on_past_tense('εκανε', 'κάνω')
        self.assertEqual('έκανε', r)

    def test_put_accent_ekaname(self):
        r = augmentify.put_accent_on_past_tense('εκαναμε', 'κάνω')
        self.assertEqual('κάναμε', r)

    def test_put_accent_hlpizame(self):
        r = augmentify.put_accent_on_past_tense('ηλπιζαμε', 'ελπίζω')
        self.assertEqual('ελπίζαμε', r)