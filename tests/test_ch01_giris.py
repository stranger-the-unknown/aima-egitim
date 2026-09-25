"""Bölüm 1: ELIZA ve modele dayalı süpürge ajanı."""
from yardimci import yukle

eliza = yukle("ch01-giris/ornekler/eliza_mini.py")
supurge = yukle("ch01-giris/cozumler/alistirma4_modelli_supurge.py")


def test_eliza_zamir_yansitma():
    e = eliza.Eliza()
    assert e.yanitla("Kendimi çok yalnız hissediyorum.") == "Ne zamandır kendini çok yalnız hissediyorsun?"
    assert "annen" in e.yanitla("Annem beni aramıyor.")


def test_eliza_olumsuzlugu_anlamaz():
    # Kalıp "hissediyorum" arar; "hissetmiyorum" genel cevaba düşer.
    assert eliza.Eliza().yanitla("Hiçbir şey hissetmiyorum.") in eliza.VARSAYILAN


def test_cozum_a6_kurallari():
    e = eliza.Eliza()
    assert e.yanitla("Babamın arabası bozuldu.") in eliza.VARSAYILAN
    assert e.yanitla("Robot süpürgem çok iyi çalışıyor.").startswith("Makineler")


def test_modelli_ajan_daha_az_hareket_eder():
    h_refleks, _, temiz1 = supurge.calistir(supurge.basit_refleks_ajan)
    h_model, _, temiz2 = supurge.calistir(supurge.ModelliAjan())
    assert temiz1 and temiz2
    assert h_model == 1 and h_refleks > h_model
