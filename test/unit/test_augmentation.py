from unittest import TestCase
from modern_greek_accentuation import augmentify


# from icecream import ic


class Augmentation(TestCase):

    def test_hthela(self):
        al = augmentify.add_augment('θέλα')
        self.assertIn('ήθελα', al)

    def test_upofera(self):
        al = augmentify.add_augment('υποφερα')
        self.assertIn('υπέφερα', al)

    def test_prokeitai(self):
        al = augmentify.add_augment('πρόκειτο')
        self.assertIn('επρόκειτο', al)

    def test_dedomenos(self):
        al = augmentify.add_augment('δομένος')
        self.assertIn('δεδομένος', al)

    def test_sunelambana(self):
        al = augmentify.add_augment('συλλάμβανα')
        self.assertIn('συνελάμβανα', al)

    def test_pairno(self):
        # if form is identical to one of prefixes
        self.assertEqual(
            augmentify.add_augment('πάρα'),
            {'έπαρα'},
        )
        self.assertNotIn('παρέα', augmentify.add_augment('πάρα'))

    def test_airo(self):
        self.assertEqual(
            augmentify.add_augment('αίρα'),
            {'ήρα'}
        )

    def test_drw(self):
        self.assertEqual(
            augmentify.add_augment('δρασμένος'),
            {'δρασμένος', 'δεδρασμένος'}
        )

    def test_krimenos(self):
        self.assertEqual(
            augmentify.add_augment('κριμένος'),
            {'κριμένος', 'κεκριμένος'}
        )

    def test_υπάρχω(self):
        self.assertEqual(
            augmentify.add_augment('υπαρχα'),
            {'ύπαρχα', 'υπήρχα', 'υπαρχα'}
        )

    def test_διέπω(self):
        self.assertEqual(
            augmentify.add_augment('διεπα'),
            {'δίεπα', 'διείπα', 'διήπα', 'έδιεπα'}
        )

    def test_dinw(self):
        self.assertEqual(
            augmentify.add_augment('δίνα'),
            {'έδινα'}
        )

    def test_pianw(self):
        self.assertEqual(
            augmentify.add_augment('πιανα'),
            {'έπιανα', 'πίανα'}
        )

    def test_paralaba(self):
        self.assertEqual(
            augmentify.add_augment('παράλαβα'),
            {'παράλαβα', 'παρέλαβα', 'παρήλαβα', 'επαράλαβα'}
        )

    def test_parameina(self):
        self.assertEqual(
            augmentify.add_augment('παράμεινα'),
            {'επαράμεινα', 'παρέμεινα', 'παράμεινα', 'παρήμεινα'},
        )

    def test_αυξημένος(self):
        self.assertEqual(
            augmentify.add_augment('αυξημένος'),
            {'ηυξημένος', 'αυξημένος'}
        )

    def test_paresth(self):
        self.assertEqual(
            augmentify.add_augment('παράστη'),
            {'πάραστη', 'παρήστη', 'παράστη', 'παρέστη', 'επαράστη'}
            ,
            # print(set(augmentify.add_augment('παράβαλα')))
        )

    def test_synap(self):
        self.assertEqual(
            augmentify.add_augment('συναπόθανα'),
            {'εσυναπόθανα', 'συναπόθανα', 'συναπέθανα', 'συνεναπόθανα',
             'συνηπόθανα'},
        )

    def test_eyriskw(self):
        self.assertEqual(
            augmentify.add_augment('εύρα'),
            {'ηύρα'}
        )

    def test_katapsygmenos(self):
        self.assertEqual(
            augmentify.add_augment('καταψυγμένος'),
            { 'καταψυγμένος', 'κεκαταψυγμένος', 'κατεψυγμένος'}

        )

    def test_parmenos(self):
        self.assertEqual(
            augmentify.add_augment('παρμένος'),
            {'παρμένος', 'πεπαρμένος'}
        )

    def test_biasmenos(self):
        self.assertEqual(
            augmentify.add_augment('βιασμένος'),
            {'βιασμένος', 'βεβιασμένος'}
        )

    def test_metaggizw(self):
        self.assertEqual(
            augmentify.add_augment('μετάγγισα'),
            {'μετάγγισα', 'μετέγγισα', 'μετήγγισα', 'εμετάγγισα'},
        )

    def test_synkrimenos(self):
        self.assertEqual(
            augmentify.add_augment('συγκριμένος'),
            {'συγκεκριμένος', 'σεσυγκριμένος', 'συγκριμένος', 'συνεγκριμένος'}
        )

    def test_thewreito(self):
        self.assertEqual(
            augmentify.add_augment('θεωρείτο'),
            {'εθεωρείτο', 'θεωρείτο', 'θεώρειτο'}
        )

    def test_eida(self):
        self.assertEqual(
            augmentify.add_augment('ίδα'),
            {'είδα'},
        )

    def test_thwrakismenos(self):
        self.assertEqual(
            augmentify.add_augment('θωρακισμένος'),
            {'τεθωρακισμένος', 'θωρακισμένος'}
        )


class DeAugment(TestCase):

    def test_deaugment_epembh(self):
        r = augmentify.deaugment_prefixed_form('επενέβη'),
        self.assertEqual(('επεμβη',), r)

    def test_deaugment_ketepsixa(self):
        r = augmentify.deaugment_prefixed_form('κατέψυχα'),
        self.assertEqual(('καταψυχα',), r)

    def test_deaugment_sokare(self):
        r = augmentify.deaugment_prefixed_form('σόκαρε'),
        self.assertEqual(('σοκαρε',), r)

    def test_deaugment_parhggeil(self):
        r = augmentify.deaugment_prefixed_form('παρήγγειλα'),
        self.assertEqual(('παραγγειλα',), r)

    def test_deaugment_parhgagan(self):
        r = augmentify.deaugment_prefixed_form('παρηγάγανε'),
        self.assertEqual(('παραγαγανε',), r)

    def test_deaugment_parebh(self):
        r = augmentify.deaugment_prefixed_form('παρέβη'),
        self.assertEqual(('παραβη',), r, )

    def test_deaugment_enekrina(self):
        r = augmentify.deaugment_prefixed_form('ενέκρινα'),
        self.assertEqual(('εγκρινα',), r)

    def test_deaugment_enekrina(self):
        r = augmentify.deaugment_prefixed_form('εξέβαλα'),
        self.assertEqual(('εκβαλα',), r)

    def test_deaugment_past_form(self):
        r = augmentify.deaugment_past_form('έκανες', 'κάνω'),
        self.assertEqual(('κανες',), r)



