from unittest import TestCase
from modern_greek_accentuation import transcription


class TranscriptionSimple(TestCase):

    def test_Basilhs(self):
        r = transcription.simple_transcription('Βασίλης')
        self.assertEqual('Basilhs', r)

    def test_Europh(self):
        r = transcription.simple_transcription('Ευρώπη')
        self.assertEqual('Europh', r)


class TranscriptionErasmian(TestCase):

    def test_Herodotos(self):
        r = transcription.erasmian_transcription('Ἡρόδοτος')
        self.assertEqual('Herodotos', r)


class TranscriptionModern(TestCase):

    def test_Wasilis(self):
        r = transcription.modern_transcription('Βασίλης')
        self.assertEqual('Wasilis', r)

    def test_euxaristo(self):
        r = transcription.modern_transcription('ευχαριστώ')
        self.assertEqual('efcharisto', r)

    def test_dieuthinsi(self):
        r = transcription.modern_transcription('διεύθυνση')
        self.assertEqual('dhiefthinsi', r)

    def test_xrisimopoio(self):
        r = transcription.modern_transcription('χρησιμοποιώ')
        self.assertEqual('chrisimopio', r)


