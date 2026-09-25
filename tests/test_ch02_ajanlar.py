"""Bölüm 2: performans ölçütü, tablo ajanı, modele dayalı ajan."""
from yardimci import yukle

olcut = yukle("ch02-akilli-ajanlar/ornekler/performans_olcutu.py")
tablo = yukle("ch02-akilli-ajanlar/ornekler/tablo_ajan.py")
onar = yukle("ch02-akilli-ajanlar/cozumler/alistirma6_olcut_onar.py")


def test_yanlis_olcut_hileciyi_odullendirir():
    durust = olcut.simule(olcut.durust_ajan, 20)
    hileci = olcut.simule(olcut.hileci_ajan, 20)
    assert hileci["supurulen_toz"] > durust["supurulen_toz"]
    assert durust["temiz_zemin"] > hileci["temiz_zemin"]


def test_tablo_boyutu_formulu():
    assert len(tablo.tablo_olustur(4)) == tablo.tablo_boyutu(4, 4) == 340
    assert tablo.tablo_boyutu(4, 10) == 1_398_100
    assert tablo.tablo_boyutu(4, 9) == 349_524


def test_tablo_ajani_refleksle_ayni_davranir():
    ajan = tablo.TabloAjani(tablo.tablo_olustur(3))
    assert [ajan(a) for a in [("A", "Kirli"), ("A", "Temiz"), ("B", "Kirli")]] == ["Süpür", "Sağ", "Süpür"]


def test_hareket_cezasinda_modelli_ajan_kazanir():
    assert onar.simule(onar.modelli) > onar.simule(onar.durust)
