import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            saldot = {1: 10, 2: 8, 3: 0}
            return saldot.get(tuote_id, 0)

        def varasto_hae_tuote(tuote_id):
            tuotteet = {
                1: Tuote(1, "maito", 5),
                2: Tuote(2, "leipä", 3),
                3: Tuote(3, "voi", 7)
            }
            return tuotteet.get(tuote_id)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuote, jonka id on 1
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_yhden_tuotteen_ostaminen(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kahden_eri_tuotteen_ostaminen(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("matti", "54321")
        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "54321", "33333-44455", 8)

    def test_kahden_saman_tuotteen_ostaminen(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("liisa", "98765")
        self.pankki_mock.tilisiirto.assert_called_with("liisa", 42, "98765", "33333-44455", 10)

    def test_varastossa_olevan_ja_loppuneen_tuotteen_ostaminen(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(3)
        kauppa.tilimaksu("anna", "11111")
        self.pankki_mock.tilisiirto.assert_called_with("anna", 42, "11111", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("eka", "11111")
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("toka", "22222")
        
        self.pankki_mock.tilisiirto.assert_called_with("toka", 42, "22222", "33333-44455", 3)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("eka", "11111")
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("toka", "22222")
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("kolmas", "33333")
        
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_korista_toimii_oikein(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.poista_korista(2)
        kauppa.tilimaksu("test", "12345")
        
        self.pankki_mock.tilisiirto.assert_called_with("test", 42, "12345", "33333-44455", 5)
        self.varasto_mock.palauta_varastoon.assert_called()