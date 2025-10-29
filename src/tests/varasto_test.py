import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)
        self.varasto_alkusaldolla = Varasto(10, 5)
        self.varasto_neg = Varasto(-10, -10)
        self.varasto_sal = Varasto(10, 20)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_tilavuus_toimii(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_tilavuus_nolla(self):
        self.assertAlmostEqual(self.varasto_neg.tilavuus, 0)

    def test_negatiivinen_saldo_nolla(self):
        self.assertAlmostEqual(self.varasto_neg.saldo, 0)

    def test_oikea_alkusaldo(self):
        self.assertAlmostEqual(self.varasto_alkusaldolla.saldo, 5)

    def test_liian_isolla_alkusaldolla_oikea_saldo(self):
        self.assertAlmostEqual(self.varasto_sal.saldo, 10)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_lisays_ei_tee_mitaan(self):
        self.varasto_alkusaldolla.lisaa_varastoon(-1)

        self.assertAlmostEqual(self.varasto_alkusaldolla.saldo, 5)

    def test_lisaa_liikaa_saldoa_ei_mene_yli(self):
        self.varasto_alkusaldolla.lisaa_varastoon(6)

        self.assertAlmostEqual(self.varasto_alkusaldolla.saldo, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_negatiivinen_ottaminen_ei_muuta_saldoa(self):
        self.varasto_alkusaldolla.ota_varastosta(-1)

        self.assertAlmostEqual(self.varasto_alkusaldolla.saldo, 5)

    def test_liian_iso_ottaminen_nollaa_saldon(self):
        self.varasto_alkusaldolla.ota_varastosta(100)

        self.assertAlmostEqual(self.varasto_alkusaldolla.saldo, 0)

    def test_liian_iso_ottaminen_nollaa_palauttaa_lopun(self):
        saldo = self.varasto_alkusaldolla.saldo
        palautettu = self.varasto_alkusaldolla.ota_varastosta(100)

        self.assertAlmostEqual(saldo, palautettu)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_merkkijonoesitys_oikein(self):
        self.assertEqual(str(self.varasto_alkusaldolla), "saldo = 5, vielä tilaa 5")
