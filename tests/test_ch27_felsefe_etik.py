"""Bölüm 27: mahremiyet, adalet ve güvenlik örneklerinin doğrulanması."""
import math

import numpy as np
import pytest

from yardimci import yukle

mh = yukle("ch27-felsefe-etik/ornekler/mahremiyet.py")
ad = yukle("ch27-felsefe-etik/ornekler/adalet.py")
gv = yukle("ch27-felsefe-etik/ornekler/guvenlik.py")
k27 = yukle("ch27-felsefe-etik/cozumler/alistirma_kod.py")


def test_mahremiyet():
    T = mh.yapay_nufus()
    assert mh.tekil_oran(T) == pytest.approx(math.exp(-10_000 / (365 * 80 * 2)), abs=0.02)
    assert mh.k_degeri(mh.genellestir(T, 3650)) > mh.k_degeri(mh.genellestir(T, 365)) > 1
    assert mh.fark_saldirisi(81_234, 12, 81_199, 13) == pytest.approx(80_779)          # kitaptaki sayılardan
    for eps in (0.1, 1.0, 5.0):
        assert mh.log_yogunluk_farki(eps) <= eps + 1e-9                               # ε-diferansiyel mahremiyet
        assert mh.sayim_fark_saldirisi(eps) <= math.exp(eps) / (1 + math.exp(eps)) + 0.01
    P = np.random.default_rng(0).normal(size=(5, 3))
    maskeli, toplam = mh.guvenli_toplama(P)
    assert np.allclose(toplam, P.sum(axis=0)) and not np.allclose(maskeli, P)


def test_adalet():
    g, s, y = ad.kalibre_veri(n=100_000)
    o = ad.grup_olcutleri(g, s, y, 0.5)
    assert o["A"]["puan 0.6–0.7 iken gerçek oran"] == pytest.approx(o["B"]["puan 0.6–0.7 iken gerçek oran"], abs=0.02)
    assert o["B"]["yanlış pozitif"] > 2 * o["A"]["yanlış pozitif"]                    # fırsat eşitliği yok
    f = ad.farkinda_olmama()
    assert f["x + posta kodu (grup silindi)"][0] - f["x + posta kodu (grup silindi)"][1] > 0.05
    assert abs(f["yalnızca x"][0] - f["yalnızca x"][1]) < 0.02
    d = ad.orneklem_dengesizligi()
    assert d["ağırlıksız"][1] > 10 * d["ağırlıksız"][0]


def test_guvenlik():
    assert gv.olasilik(gv.arac_agaci(True)) < gv.olasilik(gv.arac_agaci(False))
    assert gv.olasilik(("VEYA", "x", [("a", 0.5), ("b", 0.5)])) == pytest.approx(0.75)
    assert gv.dusuk_etkili_yol(0)[2] == ["V"] and gv.dusuk_etkili_yol(5)[2] == []
    oyun = gv.calistir(gv.en_iyi_politika("temizlenen kir başına +1"))
    temiz = gv.calistir(gv.en_iyi_politika("kalan kir başına −1"))
    assert "dök" in oyun and "dök" not in temiz
    assert gv.tekillik_hizi() == pytest.approx(336)                                    # kitaptaki hesap
    assert k27.sorma_esigi(1.0) == pytest.approx(0.99, abs=1e-3)
