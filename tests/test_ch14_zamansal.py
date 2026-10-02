"""Bölüm 14: kitaptaki örneklerle doğrulama."""
import random

import pytest

from yardimci import yukle

zm = yukle("ch14-zamansal-olasilik/ornekler/zamansal.py")
km = yukle("ch14-zamansal-olasilik/ornekler/kalman.py")
lk = yukle("ch14-zamansal-olasilik/ornekler/lokalizasyon.py")
pf = yukle("ch14-zamansal-olasilik/ornekler/parcacik_filtresi.py")
ps = yukle("ch14-zamansal-olasilik/ornekler/pil_sensoru.py")
k14 = yukle("ch14-zamansal-olasilik/cozumler/alistirma_kod.py")

GUNLER = [True, True, False, True, True]


def test_filtreleme_ve_tahmin():
    h = zm.semsiye_hmm()
    f1, f2 = h.filtrele([True, True])
    assert f1[0] == pytest.approx(0.818, abs=5e-4)
    assert h.tahmin_adimi(f1)[0] == pytest.approx(0.627, abs=5e-4)
    assert f2[0] == pytest.approx(0.883, abs=5e-4)
    assert h.duragan_dagilim() == pytest.approx([0.5, 0.5])


def test_yumusatma():
    h = zm.semsiye_hmm()
    assert h.geri_mesajlari([True, True])[0] == pytest.approx([0.69, 0.41])
    assert h.ileri_geri([True, True])[0][0] == pytest.approx(0.883, abs=5e-4)
    # son gün için yumuşatma = filtreleme
    assert h.ileri_geri(GUNLER)[-1] == pytest.approx(h.filtrele(GUNLER)[-1])


def test_viterbi():
    h = zm.semsiye_hmm()
    yol, m = h.viterbi(GUNLER)
    assert yol == ["Yağmur", "Yağmur", "Kuru", "Yağmur", "Yağmur"]
    kitap = [(0.8182, 0.1818), (0.5155, 0.0491), (0.0361, 0.1237), (0.0334, 0.0173), (0.0210, 0.0024)]
    for (a, b), (x, y) in zip(kitap, m):
        assert x == pytest.approx(a, abs=1e-4) and y == pytest.approx(b, abs=1e-4)


def test_olabilirlik():
    h = zm.semsiye_hmm()
    toplam = 0.0
    import itertools
    for dizi in itertools.product((True, False), repeat=3):
        toplam += h.olabilirlik(list(dizi))
    assert toplam == pytest.approx(1.0)


def test_kalman():
    mu, var = km.kalman_1b(0.0, 1.5 ** 2, 2.5, 2.0 ** 2, 1.0 ** 2)
    assert mu == pytest.approx(2.155, abs=5e-4) and var == pytest.approx(0.862, abs=5e-4)
    v = 2.25
    for _ in range(20):
        _, v = km.kalman_1b(0.0, v, 0.0, 4.0, 1.0)
    assert v == pytest.approx(km.sabit_varyans(4.0, 1.0))


def test_lokalizasyon():
    h, kareler = lk.konum_hmm(0.0)
    assert len(kareler) == 45 and h.onsel[0] == pytest.approx(1 / 45)
    hata, _ = lk.konum_hatasi(0.0, 20, 5)
    assert hata[-1] < hata[0]


def test_parcacik_filtresi():
    rng = random.Random(0)
    kesin = [f[0] for f in zm.semsiye_hmm().filtrele(GUNLER)]
    tahmin = pf.parcacik_filtresi(GUNLER, 20000, rng)
    assert tahmin == pytest.approx(kesin, abs=0.02)


def test_pil_sensoru():
    e, _ = ps.izle("gauss", ps.GECICI)
    assert e[7] < 1.0                     # Gauss modeli tek 0'da pilin bittiğine inanır
    e, _ = ps.izle("gecici", ps.GECICI)
    assert min(e) > 4.0                   # geçici model kısa aksaklığı atlatır
    e, _ = ps.izle("gecici", ps.KALICI)
    assert e[-1] < 0.5                    # ama kalıcı bozulmada karamsar
    e, bozuk = ps.izle("kalici", ps.KALICI)
    assert e[-1] > 4.5 and bozuk[-1] > 0.99


def test_cozumler():
    assert k14.a2() == pytest.approx(0.1907, abs=1e-4)
    p, b = k14.a4()
    assert b == pytest.approx([0.31, 0.59]) and p == pytest.approx(0.799, abs=1e-3)
    dizi, yol, argmax, _ = k14.a5()
    assert dizi == [False, True, False] and yol != argmax
    r = k14.a6()
    assert r["0.7 / 0.2"][0] == pytest.approx(0.4) and r["0.9 / 0.1"][1] > r["0.7 / 0.3"][1]
    mu2, var2 = k14.a7()
    assert mu2 == pytest.approx(1.197, abs=1e-3) and var2 == pytest.approx(0.829, abs=1e-3)
    r = k14.a10(500)
    assert max(r, key=r.get) == 0.9
