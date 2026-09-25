"""Bölüm 12: kitaptaki örneklerle doğrulama."""
from fractions import Fraction

import pytest

from yardimci import yukle

ol = yukle("ch12-belirsiz-bilgi/ornekler/olasilik.py")
dh = yukle("ch12-belirsiz-bilgi/ornekler/dis_hekimi.py")
bk = yukle("ch12-belirsiz-bilgi/ornekler/bayes_kurali.py")
hk = yukle("ch12-belirsiz-bilgi/ornekler/hollanda_kitabi.py")
wo = yukle("ch12-belirsiz-bilgi/ornekler/wumpus_olasilik.py")
nb = yukle("ch12-belirsiz-bilgi/ornekler/naive_bayes_mini.py")
k12 = yukle("ch12-belirsiz-bilgi/cozumler/alistirma_kod.py")


def test_zarlar():
    z = ol.iki_zar()
    assert z.P(lambda d: d["Zar1"] + d["Zar2"] == 11) == Fraction(1, 18)
    assert z.P(lambda d: d["Zar1"] == d["Zar2"], {"Zar1": 5}) == Fraction(1, 6)
    assert z.bagimsiz_mi("Zar1", "Zar2")


def test_dis_hekimi():
    d = dh.dis_dagilimi()
    assert d.P({"Cavity": True}) == pytest.approx(0.2)
    assert d.P(lambda w: w["Cavity"] or w["Toothache"]) == pytest.approx(0.28)
    p = d.kosullu("Cavity", {"Toothache": True})
    assert p[True] == pytest.approx(0.6) and p[False] == pytest.approx(0.4)
    p2 = d.kosullu("Cavity", {"Toothache": True, "Catch": True})
    assert p2[True] == pytest.approx(0.871, abs=5e-4)
    assert not d.bagimsiz_mi("Toothache", "Catch")
    assert d.bagimsiz_mi("Toothache", "Catch", "Cavity")
    assert len(d.carp(dh.HAVA).tablo) == 32


def test_bayes():
    assert bk.menenjit() == pytest.approx(0.0014)
    assert bk.menenjit_salgin(1) == pytest.approx(0.0014)
    assert bk.dis_naif_bayes()[0] == pytest.approx(0.108 / 0.124)


def test_hollanda_kitabi():
    tablo = hk.kazanc_tablosu({"a": 0.4, "b": 0.3, "a∧b": 0.0, "a∨b": 0.8},
                              [("a", True, 4), ("b", True, 3), ("a∨b", False, 2)])
    assert [round(tablo[s]) for s in [(True, True), (True, False), (False, True), (False, False)]] == [-11, -1, -1, -1]
    assert all(v == pytest.approx(-0.1) for v in k12.a5().values())


def test_wumpus():
    assert wo.sinir() == [(1, 3), (2, 2), (3, 1)]
    assert wo.sinir_toplami((1, 3)) == pytest.approx(0.31, abs=0.005)
    assert wo.sinir_toplami((3, 1)) == pytest.approx(0.31, abs=0.005)
    assert wo.sinir_toplami((2, 2)) == pytest.approx(0.86, abs=0.005)
    tam, terim = wo.tam_toplam((1, 3))
    assert terim == 4096 and tam == pytest.approx(wo.sinir_toplami((1, 3)))
    # açıklayıp götürme: [1,3] esintisiz çıkarsa [2,2] kesin, [3,1] önsele döner
    gozlem = {**wo.KITAP_GOZLEM, (1, 3): False}
    assert wo.sinir_toplami((2, 2), gozlem) == pytest.approx(1.0)
    assert wo.sinir_toplami((3, 1), gozlem) == pytest.approx(0.2)


def test_naif_bayes_metin():
    model = nb.egit(nb.EGITIM)
    assert nb.tahmin(model, "bedava kredi kazan")[0] == "spam"
    assert nb.tahmin(model, "yarın toplantı raporu")[0] == "ham"


def test_cozumler():
    r = k12.a4()
    assert r["P(cavity | toothache ∨ catch)"] == pytest.approx(0.192 / 0.416)
    assert k12.a6()["10 kat"] == pytest.approx(0.01383, abs=1e-5)
    assert k12.naif_bayes({"gol": True, "maç": True, "borsa": False})["spor"] == pytest.approx(0.1188 / 0.11916)
    eu = k12.beklenen_fayda(1000)
    assert max(eu, key=eu.get) == "A90"
    eu = k12.beklenen_fayda(10000)
    assert max(eu, key=eu.get) == "A180"
    assert k12.a9()[0.5] == pytest.approx((0.6, 0.8))
    r = k12.a10()
    assert not r["koşullu bağımsız mı"] and r["kesin"] == pytest.approx(0.14 / 0.156)
