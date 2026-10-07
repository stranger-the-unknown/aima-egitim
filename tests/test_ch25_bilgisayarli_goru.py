"""Bölüm 25: görüntü oluşumu, basit özellikler ve tespit özelliklerinin doğrulanması."""
import math

import numpy as np
import pytest

from yardimci import yukle

go = yukle("ch25-bilgisayarli-goru/ornekler/goruntu_olusumu.py")
oz = yukle("ch25-bilgisayarli-goru/ornekler/ozellikler.py")
ts = yukle("ch25-bilgisayarli-goru/ornekler/tespit.py")
k25 = yukle("ch25-bilgisayarli-goru/cozumler/alistirma_kod.py")


def test_goruntu_olusumu():
    assert go.perspektif((1, 0.5, 2)) == (-0.5, -0.25)                     # ters döner
    assert go.perspektif((1, 0.5, 4))[0] == pytest.approx(-0.25)            # uzaklık 2 kat → boy yarı
    assert go.kaybolma_noktasi((1, 0, 2), f=2) == (1.0, 0.0)                # (fU/W, fV/W)
    uzak = go.perspektif(go.dogru_uzerinde((5, 3, 1), (1, 0, 2), 1e7), f=2, ters=False)
    assert uzak == pytest.approx((1.0, 0.0), abs=1e-5)
    assert go.lambert(0.8, 100, 60) == pytest.approx(40.0)                  # I = ρ I₀ cos θ
    dtheta = math.radians(5 / 3600)
    assert 10 * go.ayirt_edilebilir_derinlik(100, 6, dtheta) == pytest.approx(0.4, abs=0.01)    # kitap: 0.4 mm
    assert 10 * go.ayirt_edilebilir_derinlik(30, 6, dtheta) == pytest.approx(0.036, abs=0.001)  # kitap: 0.036 mm
    T = (0.3, -0.2, 2.0)
    foe = go.genisleme_odagi(T)
    assert go.optik_akis(*foe, 7.0, T) == pytest.approx((0.0, 0.0))         # genişleme odağında akış yok
    assert go.optik_akis(0.2, 0.1, 10, T) == pytest.approx(go.optik_akis(0.2, 0.1, 20, tuple(2 * t for t in T)))


def test_kenar_doku_akis():
    I = oz.basamak()
    assert len(oz.kenar_1b(I, None)) > 3                                    # gürültü sahte tepeler üretir
    assert oz.kenar_1b(I, 2) == [50]                                        # düzeltince yalnızca gerçek kenar
    G = oz.gauss(2)
    assert np.allclose(np.convolve(np.convolve(I, G), oz.turev()), np.convolve(I, np.convolve(G, oz.turev())))
    K = oz.kare_goruntu()
    M, T = oz.gradyan(K)
    M2, T2 = oz.gradyan(0.3 * K)
    s = M > 0.2
    assert np.allclose(T[s], T2[s]) and np.allclose(M2, 0.3 * M)            # yön ışıktan bağımsız
    h = oz.yon_histogrami(oz.cizgiler())
    assert h[0] == pytest.approx(0.5, abs=0.05) and h[4] == pytest.approx(0.5, abs=0.05)
    assert np.allclose(h, oz.yon_histogrami(0.2 * oz.cizgiler() + 0.1))
    rng = np.random.default_rng(1)
    D = rng.random((40, 40))
    assert oz.ssd_akis(D, oz.kaydir(D, 3, -2), (20, 20))[0] == (3, -2)
    assert set(k25.a7()["dikey çizgiler, SSD = 0 olan adaylar"]) == {(0, d) for d in range(-5, 6)}


def test_bolutleme():
    I, g = oz.iki_bolgeli(egim=0.8)
    assert oz.dogruluk(oz.normallestirilmis_kesme(I), g) > 0.95
    assert oz.en_iyi_esik(I, g) < 0.93


def test_tespit():
    sonuc = k25.a9()
    assert sonuc["yatay çubuk"] == (0.0, 0.0) and sonuc["artı"][1] > 0 and sonuc["L köşesi"][1] == 0
    assert ts.dikdortgen_sayisi(100) == 25_502_500
    assert ts.capa_kutusu_sayisi(640, 480) == 10_800
    assert ts.iou((0, 0, 4, 4), (2, 2, 6, 6)) == pytest.approx(1 / 7)
    assert ts.nms(ts.ORNEK_KUTULAR, ts.ORNEK_PUANLAR) == [0, 3, 4]
    assert k25.a10()["kesinlik, duyarlılık (puan > 0.5)"] == pytest.approx((1.0, 2 / 3))
