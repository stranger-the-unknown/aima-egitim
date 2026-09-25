"""Bölüm 8: kitaptaki değerlerle doğrulama."""
from itertools import product

from yardimci import yukle

fm = yukle("ch08-birinci-derece-mantik/ornekler/fol_model.py")
tt = yukle("ch08-birinci-derece-mantik/ornekler/tam_toplayici.py")
ak = yukle("ch08-birinci-derece-mantik/ornekler/akrabalik_turkce.py")
ib = yukle("ch08-birinci-derece-mantik/cozumler/alistirma10_iki_bit.py")
ye = yukle("ch08-birinci-derece-mantik/cozumler/alistirma7_yegen_eniste.py")


def test_tam_toplayici_kitap_sorgusu():
    assert sorted(tt.sorgu(0, 1)) == [(0, 1, 1), (1, 0, 1), (1, 1, 0)]


def test_tam_toplayici_dogru_toplar():
    assert tt.dogrula() == []
    for g in product((0, 1), repeat=3):
        assert tt.cikislar(g) == (sum(g) % 2, sum(g) // 2)


def test_iki_bit_toplayici():
    assert ib.dogrula() == []
    assert len(ib.dogrula(bozuk=True)) == 24


def test_klasik_hatalar_ve_dogru_bicimler():
    sonuc = {metin.split("[")[0].strip(): f() for metin, f in fm.CUMLELER}
    assert sonuc["∀x Kral(x) ⇒ Kişi(x)"] is True
    assert sonuc["∀x Kral(x) ∧ Kişi(x)"] is False
    assert sonuc["∃x Taç(x) ∧ Başında(x, John)"] is True
    assert sonuc["∃x Taç(x) ⇒ Başında(x, John)"] is True


def test_niceleyici_sirasi_ve_veritabani_anlami():
    modeller = {ad: (a, b) for ad, a, b in fm.niceleyici_sirasi()}
    assert modeller["herkes başka birini seviyor"] == (True, False)
    assert fm.veritabani_modelleri() == 16


def test_akrabalik():
    assert ak.dayi("Ahmet", "Ece") and not ak.amca("Ahmet", "Ece")
    assert ak.amca("Mehmet", "Deniz") and ak.dayi("Mehmet", "Ece")
    assert ak.hala("Zeynep", "Deniz") and ak.teyze("Ayşe", "Can")
    assert all(ak.teoremler().values())
    # İngilizce 'uncle' = amca ∪ dayı
    assert set(ak.hepsi(ak.uncle)) == set(ak.hepsi(ak.amca)) | set(ak.hepsi(ak.dayi))


def test_yegen_eniste_yenge():
    assert ye.eniste("Ali", "Deniz") and ye.eniste("Ali", "Ahmet")
    assert ye.yenge("Elif", "Ece") and ye.yegen("Ece", "Ahmet")
