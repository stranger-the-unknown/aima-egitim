"""Bölüm 16: kitaptaki değerlerle doğrulama."""
import itertools
import random
from fractions import Fraction

import pytest

from yardimci import yukle

fk = yukle("ch16-basit-kararlar/ornekler/fayda_kurami.py")
il = yukle("ch16-basit-kararlar/ornekler/iyimserlik_laneti.py")
ka = yukle("ch16-basit-kararlar/ornekler/karar_agi.py")
bd = yukle("ch16-basit-kararlar/ornekler/bilgi_degeri.py")
bt = yukle("ch16-basit-kararlar/ornekler/bilinmeyen_tercihler.py")
k16 = yukle("ch16-basit-kararlar/cozumler/alistirma_kod.py")


def test_yarisma():
    kumar = [(0.5, 0), (0.5, 2_500_000)]
    assert fk.beklenen(kumar) == 1_250_000
    U = {0: 5, 2_500_000: 9, 1_000_000: 8}
    assert fk.beklenen(kumar, U.get) == 7 < U[1_000_000]


def test_beard_ve_risk():
    assert fk.beard_ters(fk.beard(123_456)) == pytest.approx(123_456)
    kucuk = fk.kesinlik_esdegeri([(0.5, 0), (0.5, 1000)], fk.beard, fk.beard_ters)
    buyuk = fk.kesinlik_esdegeri([(0.5, 0), (0.5, 800_000)], fk.beard, fk.beard_ters)
    assert 498 < kucuk < 500                     # neredeyse risk-nötr
    assert 200_000 < buyuk < 250_000             # belirgin biçimde riskten kaçınan


def test_paradokslar_ve_para_pompasi():
    assert not fk.allais_tutarli_mi()
    assert not fk.ellsberg_tutarli_mi()
    yol, odenen = fk.para_pompasi({"C": "B", "B": "A", "A": "C"}, "C", tur=1)
    assert yol[0] == yol[-1] and odenen == pytest.approx(0.03)


def test_iyilestiricinin_laneti():
    assert il.en_buyugun_ortalamasi(1) == pytest.approx(0.0, abs=1e-6)
    assert il.en_buyugun_ortalamasi(3) == pytest.approx(0.85, abs=0.01)
    assert il.en_buyugun_ortalamasi(30) == pytest.approx(2.0, abs=0.06)
    assert il.simule_et(3, deneme=50_000) == pytest.approx(il.en_buyugun_ortalamasi(3), abs=0.02)


def test_baskinlik_ve_karar_agi():
    assert ka.stokastik_baskin_mi((2.8, 4.8), (3.0, 5.2))
    assert not ka.stokastik_baskin_mi((3.0, 5.2), (2.8, 4.8))
    en_iyi, eu = ka.en_iyi_yer()
    assert en_iyi == "S1" and set(eu) == set(ka.YERLER)
    p = ka.P_TRAFIK_YOGUN
    for y in ka.YERLER:   # trafiğe göre koşullu EU'ların ortalaması koşulsuz EU'yu verir
        assert ka.beklenen_fayda(y) == pytest.approx(
            p * ka.beklenen_fayda(y, trafik_bilgisi=True) + (1 - p) * ka.beklenen_fayda(y, trafik_bilgisi=False))


def test_petrol_vpi():
    for n in (3, 4, 7, 10):
        assert bd.petrol(n).vpi(["araştırma(3)"]) == Fraction(1, n)


def test_vpi_ozellikleri():
    t = bd.tibbi()
    v1, v1b, v2 = t.vpi(["T1"]), t.vpi(["T1b"]), t.vpi(["T2"])
    assert min(v1, v2) >= 0
    assert t.vpi(["T1", "T1b"]) < v1 + v1b                       # toplamsal değil
    sira1 = v1 + sum(t.gozlem_olasiligi({}, {"T1": o}) * t.vpi(["T2"], {"T1": o}) for o in "+−")
    sira2 = v2 + sum(t.gozlem_olasiligi({}, {"T2": o}) * t.vpi(["T1"], {"T2": o}) for o in "+−")
    assert sira1 == pytest.approx(sira2) == pytest.approx(t.vpi(["T1", "T2"]))   # sıradan bağımsız
    assert bd.vpi_gauss(5, 1, 0) < 1e-5 < bd.vpi_gauss(0.1, 0.2, 0) < bd.vpi_gauss(0.1, 3, 0)
    adimlar = bd.miyop_ajan(t, {"T1": 1.0, "T1b": 1.0, "T2": 0.5}, "hasta", random.Random(4))
    assert adimlar[-1][0] == "karar"


def test_bilinmeyen_tercihler():
    assert bt.durian() == {"vanilya": 1.0, "durian": 8.0}
    d = bt.tekduze_oyun(-40, 60)
    assert d == {"hemen yap": 10.0, "kendini kapat": 0.0, "bekle": 18.0}
    for mu, s in ((10, 20), (-5, 3), (0, 1)):
        n = bt.normal_oyun(mu, s)
        assert n["bekle"] >= max(n["hemen yap"], 0)
    assert bt.normal_oyun(10, 0)["bekle"] == 10


def test_cozumler():
    a4 = k16.a4()
    assert a4["araba mikromortu"] == 400 and a4["$/mikromort"] == pytest.approx(60)
    assert k16.allais_araligi(0.0) is None
    assert k16.allais_araligi(0.25) == pytest.approx((0.75, 0.8))
    a6 = k16.a6(deneme=5000)
    assert a6["Bayes: seçilenin gerçek değeri"] > a6["saf: seçilenin gerçek değeri"]
    assert a6["saf: seçilenin tahmini"] - a6["saf: seçilenin gerçek değeri"] > 3
    a7 = k16.a7()
    assert a7["VPI(HavaTrafiği)"] == pytest.approx(0.0, abs=1e-9)
    assert a7["sağlam karar"] == "S1"
    assert k16.a10()["bekle(ε)"][0.0] == pytest.approx(18.0)
    assert k16.hatali_harriet(-40, 60, 8 / 26)["bekle"] == pytest.approx(10.0)


def test_hazine_avi_pc_sirasi():
    """Kitap: en iyi sıra yerleri P(i)/C(i)'ye göre büyükten küçüğe dizer."""
    rng = random.Random(16)
    for _ in range(30):
        n = 5
        P = [rng.uniform(0.05, 0.9) for _ in range(n)]
        C = [rng.uniform(0.5, 10) for _ in range(n)]
        pc = sorted(range(n), key=lambda i: -P[i] / C[i])
        en_iyi = min(k16.beklenen_maliyet(s, P, C) for s in itertools.permutations(range(n)))
        assert k16.beklenen_maliyet(pc, P, C) == pytest.approx(en_iyi)
