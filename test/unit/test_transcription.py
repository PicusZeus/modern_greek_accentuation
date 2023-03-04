from unittest import TestCase
from modern_greek_accentuation import transcription


class TranscriptionSimple(TestCase):

    def test_mow(self):
        r = transcription.simple_transcription('μοβ')
        self.assertEqual('mob', r)

    def test_Basilhs(self):
        r = transcription.simple_transcription('Βασίλης')
        self.assertEqual('Basilhs', r)

    def test_Europh(self):
        r = transcription.simple_transcription('Ευρώπη')
        self.assertEqual('Europh', r)

    def test_exo(self):
        r = transcription.simple_transcription('έχω')
        self.assertEqual('echo', r)

    def test_kai(self):
        r = transcription.simple_transcription('και')
        self.assertEqual('kai', r)

    def test_thumamai(self):
        r = transcription.simple_transcription('θυμάμαι')
        self.assertEqual('thumamai', r)

    def test_koulouri(self):
        r = transcription.simple_transcription('κουλούρι')
        self.assertEqual('koulouri', r)


class TranscriptionErasmian(TestCase):

    def test_Herodotos(self):
        r = transcription.erasmian_transcription('Ἡρόδοτος')
        self.assertEqual('Herodotos', r)

    def test_exo(self):
        r = transcription.erasmian_transcription('έχω')
        self.assertEqual('echo', r)

    def test_kai(self):
        r = transcription.erasmian_transcription('και')
        self.assertEqual('kai', r)

class TranscriptionModern(TestCase):

    def test_Wasilis(self):
        r = transcription.modern_transcription('Βασίλης')
        self.assertEqual('Wasilis', r)

    def test_mow(self):
        r = transcription.modern_transcription('μοβ')
        self.assertEqual('mof', r)

    def test_euxaristo(self):
        r = transcription.modern_transcription('ευχαριστώ')
        self.assertEqual('efcharisto', r)

    def test_dieuthinsi(self):
        r = transcription.modern_transcription('διεύθυνση')
        self.assertEqual('dhiefthinsi', r)

    def test_xrisimopoio(self):
        r = transcription.modern_transcription('χρησιμοποιώ')
        self.assertEqual('chrisimopio', r)

    def test_exo(self):
        r = transcription.modern_transcription('έχω')
        self.assertEqual('echo', r)

    def test_kai(self):
        r = transcription.modern_transcription('και')
        self.assertEqual('kie', r)


