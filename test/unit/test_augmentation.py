from unittest import TestCase
from modern_greek_accentuation import augmentify


# from icecream import ic


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

    def test_pairno(self):
        # if form is identical to one of prefixes
        self.assertEqual(
            augmentify.add_augment('πάρα'),
            ['έπαρα'],
        )
        self.assertNotIn('παρέα', augmentify.add_augment('πάρα'))

    def test_airo(self):
        self.assertEqual(
            set(augmentify.add_augment('αίρα')),
            {'ήιρα', 'ήρα'}
        )

    def test_drw(self):
        self.assertEqual(
            set(augmentify.add_augment('δρασμένος')),
            {'δρασμένος', 'δεδρασμένος'}
        )

    def test_krimenos(self):
        self.assertEqual(
            set(augmentify.add_augment('κριμένος')),
            {'κριμένος', 'κεκριμένος'}
        )

    def test_υπάρχω(self):
        self.assertEqual(
            set(augmentify.add_augment('υπαρχα')),
            {'ύπαρχα', 'υπήρχα', 'εύπαρχα', 'υπαρχα'}
        )

    def test_διέπω(self):
        self.assertEqual(
            set(augmentify.add_augment('διεπα')),
            {'δίεπα', 'διείπα', 'έδιεπα', 'διήπα'}
        )

    def test_dinw(self):
        self.assertEqual(
            set(augmentify.add_augment('δινα')),
            {'δίεπα', 'διείπα', 'έδιεπα', 'διήπα'}
        )

    def test_pianw(self):
        self.assertEqual(
            set(augmentify.add_augment('πιανα')),
            {'έπιανα', 'πίανα'}
        )

    def test_paralaba(self):
        self.assertEqual(
            set(augmentify.add_augment('παράλαβα')),
            {'παράλαβα', 'παρέλαβα','παρήλαβα','επαράλαβα'}
        )

    def test_parameina(self):
        self.assertEqual(
            set(augmentify.add_augment('παράμεινα')),
            {'επαράμεινα', 'παρέμεινα', 'παράμεινα', 'παρήμεινα'},
            # print(set(augmentify.add_augment('παράμεινα')))
        )

    def test_paresth(self):
        self.assertEqual(
            set(augmentify.add_augment('παράστη')),
            {'πάραστη', 'παρήστη', 'παράστη', 'παρέστη', 'επαράστη'}
,
            # print(set(augmentify.add_augment('παράβαλα')))
        )

    def test_synap(self):
        self.assertEqual(
            set(augmentify.add_augment('συναπόθανα')),
            {'συνεναπόθανα', 'εσυναπόθανα', 'συναπόθανα', 'συναπέθανα', 'συεναπόθανα', 'συνεαπόθανα',
             'συναποέθανα'},
        )

    def test_eyriskw(self):
        self.assertEqual(
            set(augmentify.add_augment('εύρα')),
            {'ηυρα'}
        )

    def test_parmenos(self):
        self.assertEqual(
            set(augmentify.add_augment('παρμένος')),
            {'παρμένος', 'πεπαρμένος'}
        )

    def test_biasmenos(self):
        self.assertEqual(
            set(augmentify.add_augment('βιασμένος')),
            {'βιασμένος', 'βεβιασμένος'}
        )

    def test_metaggizw(self):
        self.assertEqual(
            set(augmentify.add_augment('μετάγγισα')),
            {'μετάγγισα', 'μεταέγγισα', 'μετέγγισα', 'μετήγγισα', 'εμετάγγισα'},
        )

    def test_thwrakismenos(self):
        self.assertEqual(
            set(augmentify.add_augment('θωρακισμένος')),
            {'τεθωρακισμένος', 'θωρακισμένος'}

        )


class DeAugment(TestCase):

    def test_deaugment_epembh(self):
        r = augmentify.deaugment_prefixed_stem('επενέβη'),
        self.assertEqual(('επεμβη',), r)

    def test_deaugment_parhggeil(self):
        r = augmentify.deaugment_prefixed_stem('παρήγγειλα'),
        self.assertEqual(('παραγγειλα',), r)

    def test_deaugment_parhgagan(self):
        r = augmentify.deaugment_prefixed_stem('παρηγάγανε'),
        self.assertEqual(('παραγάγανε',), r)

    def test_deaugment_parebh(self):
        r = augmentify.deaugment_prefixed_stem('παρέβη'),
        self.assertEqual(('παραβη',), r, )

    def test_deaugment_enekrina(self):
        r = augmentify.deaugment_prefixed_stem('ενέκρινα'),
        self.assertEqual(('εγκρινα',), r)

    def test_deaugment_enekrina(self):
        r = augmentify.deaugment_prefixed_stem('εξέβαλα'),
        self.assertEqual(('εκβαλα',), r)

    def test_deaugment_past_form(self):
        r = augmentify.deaugment_past_form('έκανες', 'κάνω'),
        self.assertEqual(('κανες',), r)


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
