"""Bölüm 13: kitaptaki örneklerle doğrulama."""
import random

import pytest

from yardimci import yukle

ba = yukle("ch13-olasiliksal-akil/ornekler/bayes_agi.py")
ha = yukle("ch13-olasiliksal-akil/ornekler/hirsiz_alarmi.py")
yd = yukle("ch13-olasiliksal-akil/ornekler/yerel_dagilimlar.py")
ok = yukle("ch13-olasiliksal-akil/ornekler/ornekleme.py")
nd = yukle("ch13-olasiliksal-akil/ornekler/nedensel.py")
k13 = yukle("ch13-olasiliksal-akil/cozumler/alistirma_kod.py")

T, F = True, False
JM = {"JohnCalls": T, "MaryCalls": T}


def test_ortak_olasilik():
    ag = ha.hirsiz_agi()
    olay = {"JohnCalls": T, "MaryCalls": T, "Alarm": T, "Burglary": F, "Earthquake": F}
    assert ag.ortak(olay) == pytest.approx(0.90 * 0.70 * 0.001 * 0.999 * 0.998)
    assert ag.ortak(olay) == pytest.approx(0.000628, abs=5e-7)
    assert ag.parametre_sayisi() == 10


def test_hirsiz_sorgusu():
    ag = ha.hirsiz_agi()
    ham = ag.numaralandirma("Burglary", JM, ham=True)
    assert ham[T] == pytest.approx(0.00059224, abs=1e-8)
    assert ham[F] == pytest.approx(0.0014919, abs=1e-7)
    for sonuc in (ag.numaralandirma("Burglary", JM), ag.degisken_eleme("Burglary", JM)):
        assert sonuc[T] == pytest.approx(0.284, abs=5e-4)
    # açıklayıp götürme
    assert ag.degisken_eleme("Burglary", {"Alarm": T})[T] > 0.3
    assert ag.degisken_eleme("Burglary", {"Alarm": T, "Earthquake": T})[T] < 0.01


def test_eleme_numaralandirma_ayni():
    ag = ok.yagmurlama_agi()
    for X, e in [("Rain", {"Sprinkler": T}), ("Cloudy", {"WetGrass": T}), ("Sprinkler", {"WetGrass": T, "Rain": F})]:
        assert ag.degisken_eleme(X, e)[T] == pytest.approx(ag.numaralandirma(X, e)[T])


def test_dugum_sirasi():
    ag = ha.hirsiz_agi()
    sayilar = []
    for sira in (["Burglary", "Earthquake", "Alarm", "JohnCalls", "MaryCalls"],
                 ["MaryCalls", "JohnCalls", "Alarm", "Burglary", "Earthquake"],
                 ["MaryCalls", "JohnCalls", "Earthquake", "Burglary", "Alarm"]):
        sayilar.append(sum(2 ** len(v) for v in ha.minimal_ebeveynler(ag, sira).values()))
    assert sayilar == [10, 13, 31]


def test_markov_ortusu():
    ag = ha.hirsiz_agi()
    assert ag.markov_ortusu("Burglary") == {"Alarm", "Earthquake"}
    assert ag.markov_ortusu("Alarm") == {"Burglary", "Earthquake", "JohnCalls", "MaryCalls"}


def test_gurultulu_or():
    cpt = ba.gurultulu_or(yd.Q_ATES)
    beklenen = {(F, F, F): 0.0, (F, F, T): 0.9, (F, T, F): 0.8, (F, T, T): 0.98,
                (T, F, F): 0.4, (T, F, T): 0.94, (T, T, F): 0.88, (T, T, T): 0.988}
    for k, v in beklenen.items():
        assert cpt[k] == pytest.approx(v)
    assert yd.probit(6) == pytest.approx(0.5) and yd.expit(6) == pytest.approx(0.5)


def test_ornekleme():
    ag = ok.yagmurlama_agi()
    assert ag.ortak({"Cloudy": T, "Sprinkler": F, "Rain": T, "WetGrass": T}) == pytest.approx(0.324)
    assert ag.numaralandirma("Rain", {"Sprinkler": T})[T] == pytest.approx(0.3)
    rng = random.Random(0)
    tahmin, _ = ag.ret_ornekleme("Rain", {"Sprinkler": T}, 20000, rng)
    assert tahmin[T] == pytest.approx(0.3, abs=0.03)
    kesin = ag.numaralandirma("Rain", {"Cloudy": T, "WetGrass": T})[T]
    assert ag.olabilirlik_agirliklandirma("Rain", {"Cloudy": T, "WetGrass": T}, 20000, rng)[T] == pytest.approx(kesin, abs=0.02)
    kesin = ag.numaralandirma("Rain", {"Sprinkler": T, "WetGrass": T})[T]
    assert ag.gibbs("Rain", {"Sprinkler": T, "WetGrass": T}, 50000, rng, isinma=100)[T] == pytest.approx(kesin, abs=0.03)


def test_nedensel():
    ag = ok.yagmurlama_agi()
    assert ag.mudahale("Sprinkler", T).numaralandirma("Rain", {})[T] == pytest.approx(0.5)
    mud = ag.mudahale("Sprinkler", T).numaralandirma("WetGrass", {})[T]
    assert nd.arka_kapi_ayarlamasi(ag, "Cloudy") == pytest.approx(mud)
    assert nd.arka_kapi_ayarlamasi(ag, "Rain") == pytest.approx(mud)


def test_cozumler():
    assert k13.a4()["elle"] == pytest.approx(k13.a4()["kod"])
    r = k13.a5()
    assert (r["S ⊥ R"], r["S ⊥ R | C"], r["S ⊥ R | C, W"], r["C ⊥ W | S, R"]) == (False, True, False, True)
    assert [n for n, _ in k13.a6().values()] == [9, 11]
    assert k13.a7()["P(öksürük | ¬soğuk, grip, alerji)"] == pytest.approx(0.88)
    assert "MaryCalls" not in k13.a8()["ilgili"]
    r = k13.a9()
    assert r["P(S = true)"] == pytest.approx(9 / 16) and r["kaba kuvvet"] == 9
