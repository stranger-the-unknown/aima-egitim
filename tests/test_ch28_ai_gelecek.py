"""Bölüm 28: kaba kuvvetin sınırları, eğilimler ve düşünmeyi denetleme örneklerinin doğrulanması."""
import pytest

from yardimci import yukle

hs = yukle("ch28-AI-gelecek/ornekler/hesaplama_sinirlari.py")
k28 = yukle("ch28-AI-gelecek/cozumler/alistirma_kod.py")


def test_borges_ve_egilimler():
    assert hs.borges() == 11                                                 # kitap: bir yılda yalnızca 11 sözcük
    assert hs.katlanma_suresi(2 ** 4, 8) == pytest.approx(2.0)                # arXiv: iki yılda bir ikiye
    assert hs.katlanma_suresi(1e10, 50) == pytest.approx(1.505, abs=1e-3)


def test_dusunmeyi_denetlemek():
    h = [e for _, e in hs.anytime_tahmin()]
    assert h[-1] < h[0]                                                       # zamanla nitelik artar
    assert hs.hesaplama_degeri(0.0, 1.0, 5.0, 1.0) < 1e-3 < hs.hesaplama_degeri(0.0, 1.0, 0.0, 1.0)
    az, _, _ = hs.ustakil_karar(0.1)
    cok, _, _ = hs.ustakil_karar(0.001)
    assert cok > az                                                           # ucuz hesaplama → daha çok düşün
    assert hs.en_iyi_derinlik(1e-6)[0] > hs.en_iyi_derinlik(1e-2)[0]
    r = k28.a5()
    assert r["ileri bakan"][2] >= r["miyop"][2]
