import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(500)

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassa, None)

    def test_luodun_kassapaatteen_rahamaara(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    #CASH:
    #edulliset:
    def test_luodun_kassapaatteen_myytyjen_edullisten_maara(self):
        self.assertEqual(self.kassa.edulliset, 0)

    def test_kassan_rahamaara_kasvaa_oikein_edulliset(self):
        self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)

    def test_vaihtorahan_maara_edulliset(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(1000), 760)

    def test_myydyt_kasvaa_edulliset(self):
        self.kassa.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_maksu_riittamaton_rahamaara_ei_muutu_edulliset(self):
        self.kassa.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_maksu_riittamaton_kaikki_rahat_palautetaan_edulliset(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(100), 100)

    def test_maksu_riittamaton_myytyjen_maara_ei_muutu_edulliset(self):
        self.kassa.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassa.edulliset, 0)

    #maukkaat:
    def test_luodun_kassapaatteen_myytyjen_maukkaiden_maara(self):
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_kassan_rahamaara_kasvaa_oikein_maukkaat(self):
        self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)

    def test_vaihtorahan_maara_maukkaat(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(1000), 600)

    def test_myydyt_kasvaa_maukkaat(self):
        self.kassa.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_maksu_riittamaton_rahamaara_ei_muutu_maukkaat(self):
        self.kassa.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_maksu_riittamaton_kaikki_rahat_palautetaan_maukkaat(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(100), 100)

    def test_maksu_riittamaton_myytyjen_maara_ei_muutu_maukkaat(self):
        self.kassa.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassa.edulliset, 0)

    #CARD:
    #edulliset:
    def test_kortti_jos_raha_riittaa_oikea_summa_veloittuu_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti), "saldo: 2.6")

    def test_kortti_jos_raha_riittaa_palautetaan_true_edulliset(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)

    def test_kortti_jos_raha_riittaa_myydyt_kasvaa_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_kortti_jos_raha_ei_riita_kortin_rahamaara_ei_muutu_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti), "saldo: 0.2")

    def test_kortti_jos_raha_ei_riita_myytyjen_maara_ei_muutu_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 2)

    def test_kortti_jos_raha_ei_riita_palautetaan_false_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), False)

    def test_kortti_kassassa_raha_ei_muutu_ostaessa_edulliset(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    #maukkaat:
    def test_kortti_jos_raha_riittaa_oikea_summa_veloittuu_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti), "saldo: 1.0")

    def test_kortti_jos_raha_riittaa_palautetaan_true_maukkaat(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)

    def test_kortti_jos_raha_riittaa_myydyt_kasvaa_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_kortti_jos_raha_ei_riita_kortin_rahamaara_ei_muutu_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti), "saldo: 1.0")

    def test_kortti_jos_raha_ei_riita_myytyjen_maara_ei_muutu_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_kortti_jos_raha_ei_riita_palautetaan_false_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), False)

    def test_kortti_kassassa_raha_ei_muutu_ostaessa_maukkaat(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    #kortin lataus:
    def test_kortille_ladattaessa_kortin_saldo_kasvaa_oikein(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(str(self.kortti), "saldo: 15.0")

    def test_kortille_ladatessa_kassan_rahamaara_kasvaa_oikein(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(self.kassa.kassassa_rahaa, 101000)

    def test_negatiivinen_lataussumma_ei_kasvata_kortin_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -10)
        self.assertEqual(str(self.kortti), "saldo: 5.0")

    def test_negatiivinen_lataussumma_ei_kasvata_kassan_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -10)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)