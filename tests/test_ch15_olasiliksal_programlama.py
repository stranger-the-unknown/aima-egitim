"""Bölüm 15: kitaptaki modellerle doğrulama."""
import random

import pytest

from yardimci import yukle

rpm = yukle("ch15-olasiliksal-programlama/ornekler/rpm_oneriler.py")
bd = yukle("ch15-olasiliksal-programlama/ornekler/beceri_derecelendirme.py")
ae = yukle("ch15-olasiliksal-programlama/ornekler/acik_evren.py")
mo = yukle("ch15-olasiliksal-programlama/ornekler/metin_okuma.py")
k15 = yukle("ch15-olasiliksal-programlama/cozumler/alistirma_kod.py")


def test_rpm_kitap_degerleri():
    assert rpm.P_HONEST == 0.99
    assert rpm.P_KINDNESS == [0.1, 0.1, 0.2, 0.3, 0.3]
    assert rpm.P_QUALITY == [0.05, 0.2, 0.4, 0.2, 0.15]
    assert rpm.DURUST_OLMAYAN == [0.4, 0.1, 0.0, 0.1, 0.4]
    assert len(rpm.temellendir(["C1", "C2", "C3"], ["B1", "B2", "B3", "B4"])) == 2 * 3 + 4 + 12
    for k in rpm.PUANLAR:
        for q in rpm.PUANLAR:
            assert sum(rpm.durust_oneri(k, q)) == pytest.approx(1.0)


def test_rpm_cikarim():
    assert rpm.ortalama(rpm.P_QUALITY) == pytest.approx(3.2)
    kanit = {("C1", "B1"): 4, ("C2", "B1"): 5, ("C3", "B1"): 4}
    s = rpm.sonsal(kanit, ["B1"])
    assert rpm.ortalama(s["kalite"]["B1"]) > 4.0
    s2 = rpm.sonsal({**kanit, ("C4", "B1"): 1, ("C4", "B2"): 5, ("C1", "B2"): 2}, ["B1", "B2"])
    assert s2["durust"]["C4"] < 0.5 < s2["durust"]["C1"]


def test_beceri():
    sonuc, beceri, w, _ = bd.sonsal_beceri(N=50_000)
    assert sonuc["Ayşe"][0] > max(sonuc[o][0] for o in ("Burak", "Ceren", "Deniz"))
    p = bd.kazanma_olasiligi(beceri, w, 0, 3)
    assert 0.5 < p < 1.0


def test_acik_evren():
    s4 = ae.login_sayisi_sonsali(4)
    assert float(sum(v for (_, d), v in s4.items() if d > 0)) == pytest.approx(1.0)
    dagilim = [float(sum(v for (m, _), v in s4.items() if m == n)) for n in (1, 2, 3)]
    assert dagilim == pytest.approx([0.169, 0.335, 0.497], abs=2e-3)
    s3 = ae.login_sayisi_sonsali(3)
    assert float(sum(v for (m, d), v in s3.items() if m == 3 and d == 0)) > 0.99
    rng = random.Random(0)
    for _ in range(50):
        d = ae.dunya_ornekle(rng)
        assert 1 <= d["#Customer"] <= 3 and 2 <= d["#Book"] <= 4
        for m in d["musteriler"]:
            assert len(m["loginler"]) == 1 if m["durust"] else 2 <= len(m["loginler"]) <= 5


def test_metin_okuma():
    rng = random.Random(0)
    g = mo.ciz("KALEM", 0.0, rng)
    assert mo.bagimsiz_oku(g, 0.01) == "KALEM" and mo.markov_oku(g, 0.01) == "KALEM"
    b, m = mo.dogruluk(0.35, deneme=10)
    assert m > b


def test_cozumler():
    r = k15.a5()
    assert r["E[Q(B1)] | C1:5"] > 4.0
    r = k15.a6()
    assert r[25.0]["Ayşe"] - r[25.0]["Burak"] > r[4.17]["Ayşe"] - r[4.17]["Burak"]
    assert k15.a9()["hipotez sayısı"] == 32
    r = k15.a10(deneme=5)
    assert r["ileri–geri harf"] >= r["Viterbi harf"] - 0.02
