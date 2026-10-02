"""Bölüm 18: kitaptaki oyunlarla doğrulama."""
from fractions import Fraction

import numpy as np
import pytest

from yardimci import yukle

ok = yukle("ch18-cok-ajanli-karar/ornekler/oyun_kurami.py")
to = yukle("ch18-cok-ajanli-karar/ornekler/tekrarli_oyunlar.py")
ub = yukle("ch18-cok-ajanli-karar/ornekler/uzun_bicim.py")
io = yukle("ch18-cok-ajanli-karar/ornekler/isbirlikci_oyunlar.py")
mt = yukle("ch18-cok-ajanli-karar/ornekler/mekanizma_tasarimi.py")
k18 = yukle("ch18-cok-ajanli-karar/cozumler/alistirma_kod.py")


def test_mahkum_ikilemi():
    assert ok.baskin_strateji(ok.MAHKUM, 0) == ok.baskin_strateji(ok.MAHKUM, 1) == "tanık"
    assert ok.saf_nash(ok.MAHKUM) == [("tanık", "tanık")]
    pareto = ok.pareto_en_iyi(ok.MAHKUM)
    assert ("tanık", "tanık") not in pareto and len(pareto) == 3
    en_iyi = max(ok.MAHKUM.profiller(), key=lambda p: (ok.faydaci_refah(ok.MAHKUM, p), ok.esitlikci_refah(ok.MAHKUM, p)))
    assert en_iyi == ("sus", "sus")


def test_koordinasyon_ve_yazi_tura():
    assert ok.baskin_strateji(ok.KOORDINASYON, 0) is None
    assert sorted(ok.saf_nash(ok.KOORDINASYON)) == [("b", "r"), ("t", "l")]
    assert ok.saf_nash(ok.YAZI_TURA) == []
    v, p, q = ok.maksimin(ok.matris(ok.YAZI_TURA))
    assert v == pytest.approx(0) and p == pytest.approx([0.5, 0.5]) and q == pytest.approx([0.5, 0.5])


def test_morra():
    A = ok.matris(ok.morra())
    assert A.tolist() == [[2, -3], [-3, 4]]
    assert ok.sirali_saf_minimaks(A) == (-3, 2)
    assert ok.iki_kere_iki_karma(A) == (Fraction(7, 12), Fraction(-1, 12))
    v, p, q = ok.maksimin(A)
    assert v == pytest.approx(-1 / 12) and p == pytest.approx([7 / 12, 5 / 12]) and q == pytest.approx([7 / 12, 5 / 12])


def test_tekrarli_oyunlar():
    eylemler, toplam = to.sonlu_geriye_tumevarim(100)
    assert set(eylemler) == {to.T} and toplam == -500
    beklenen = {("GÜVERCİN", "GÜVERCİN"): (-1, -1), ("ŞAHİN", "GÜVERCİN"): (0, -10), ("ŞAHİN", "ŞAHİN"): (-5, -5),
                ("ŞAHİN", "ACIMASIZ"): (-5, -5), ("ACIMASIZ", "ACIMASIZ"): (-1, -1)}
    ad = {m.ad: m for m in to.MAKINELER}
    for (a, b), u in beklenen.items():
        assert to.oyna(ad[a], ad[b])[2] == u
    assert to.nash_mi(to.ACIMASIZ, to.ACIMASIZ) and to.nash_mi(to.SAHIN, to.SAHIN)
    assert not to.nash_mi(to.GUVERCIN, to.GUVERCIN) and not to.nash_mi(to.SAHIN, to.ACIMASIZ)
    assert not k18.a4(0.1)["ACIMASIZ–ACIMASIZ denge mi"] and k18.a4(0.2)["ACIMASIZ–ACIMASIZ denge mi"]


def test_uzun_bicim_ve_poker():
    u, strateji = ub.geriye_tumevarim(ub.SEKIL_18_4)
    assert u == (1, 1) and strateji == {"/": "yukarı", "/yukarı": "yukarı"}
    assert sorted(ok.saf_nash(ub.sekil_18_4_normal_bicim())) == [("aşağı", "aşağı"), ("yukarı", "yukarı")]
    F = Fraction
    kitap = [[0, F(-1, 6), 1, F(7, 6)], [F(-1, 3), F(-1, 6), F(5, 6), F(2, 3)],
             [F(1, 3), 0, F(1, 6), F(1, 2)], [0, 0, 0, 0]]
    assert ub.poker_matrisi() == kitap
    dengeler = {(ub.P1_STRATEJILER[i], ub.P2_STRATEJILER[j]) for i, j in ub.saf_eyer_noktalari(kitap)}
    assert dengeler == {("rk", "cf"), ("kk", "cf")}
    assert ok.maksimin([[float(x) for x in r] for r in kitap])[0] == pytest.approx(0, abs=1e-12)


def test_atas_oyunu():
    robbie, (alt, ust) = ub.atas_dengesi()
    assert robbie == {"2 ataş": "90 ataş", "1 + 1": "50 + 50", "2 zımba": "90 zımba"}
    assert alt == pytest.approx(0.446, abs=1e-3) and ust == pytest.approx(0.554, abs=1e-3)


def test_isbirlikci_oyunlar():
    assert len(io.koalisyonlar([1, 2, 3])) == 7
    assert len(io.koalisyon_yapilari([1, 2, 3])) == 5 and len(io.koalisyon_yapilari([1, 2, 3, 4])) == 15
    bos = lambda C: 1 if len(C) >= 2 else 0
    assert io.superadditif_mi([1, 2, 3], bos) and io.cekirdek_bos_mu([1, 2, 3], bos)
    iki = lambda C: {1: 5, 2: 20}[len(C)] if C else 0
    assert io.cekirdekte_mi([1, 2], iki, {1: 6, 2: 14}) and not io.cekirdek_bos_mu([1, 2], iki)
    assert io.shapley([1, 2], iki) == {1: 10, 2: 10}
    kurallar = [({1, 2}, 5), ({2}, 2), ({3}, 4)]
    nu = io.mc_agi(kurallar)
    assert [nu(C) for C in ({1}, {3}, {1, 3}, {2, 3}, {1, 2, 3})] == [0, 4, 4, 6, 11]
    assert io.shapley([1, 2, 3], nu) == io.mc_agi_shapley([1, 2, 3], kurallar) == {1: Fraction(5, 2), 2: Fraction(9, 2), 3: 4}
    s = k18.a7()
    assert s["Shapley"] == {1: Fraction(2, 3), 2: Fraction(1, 6), 3: Fraction(1, 6)}
    assert s["çekirdek (ızgarada)"] == [(1, 0, 0)]


def test_acik_artirmalar_ve_vcg():
    assert mt.ingiliz([120, 95, 180, 150], rezerv=50, d=1) == (2, 151)       # b_o + d
    assert mt.ikinci_fiyat([120, 95, 180, 150]) == (2, 150)
    assert mt.dogruluk_baskin_mi(100, range(0, 201, 5), range(0, 201, 7))
    r = mt.reklam_yuvalari()
    assert r["dürüst (n+1 fiyat)"] == pytest.approx(1) and r["düşük teklif (n+1 fiyat)"] == pytest.approx(2)
    assert r["doğru mekanizma"] == pytest.approx(2.6)
    kazananlar, vergi = mt.vcg([100, 50, 40, 20, 10], 3)
    assert sorted(kazananlar) == [0, 1, 2] and list(vergi.values()) == [20, 20, 20]
    assert k18.a8()["dürüstlük her ajan için en iyi"]
    g = mt.gelir_esitligi(deneme=20_000)
    assert g["birinci fiyat"] == pytest.approx(0.6, abs=0.01) and g["ikinci fiyat"] == pytest.approx(0.6, abs=0.01)
    o = mt.ortak_kaynak()
    assert o == {"herkes kirletir": -104, "herkes azaltır": -10, "kirletmek baskın mı": True}


def test_oylama_ve_pazarlik():
    C = mt.CONDORCET
    assert mt.ikili(C, "a", "b") > 0 and mt.ikili(C, "b", "c") > 0 and mt.ikili(C, "c", "a") > 0
    assert mt.condorcet_kazanani(C) is None
    s = k18.a9()
    assert s["dürüst çoğunluk"] == ["A"] and s["C'ciler B'ye oy verirse"] == ["B"] and s["Condorcet"] == "C"
    assert mt.donusumlu_teklif(1, 0.9, 0.8) == 1.0
    assert mt.donusumlu_teklif(2, 0.9, 0.8) == pytest.approx(1 - 0.8)
    assert mt.donusumlu_teklif(200, 0.9, 0.8) == pytest.approx(mt.rubinstein(0.9, 0.8), abs=1e-6)
    assert mt.rubinstein(0.9, 0.9) == pytest.approx(1 / 1.9)


def test_cozumler():
    s = k18.a1()
    assert s["karma: P(kaç)"] == (Fraction(9, 10), Fraction(9, 10))
    v, p, q = ok.maksimin(k18.morra3())
    assert v == pytest.approx(0, abs=1e-12)
    assert np.all(p @ k18.morra3() >= -1e-9)          # E'nin stratejisi her O eylemine karşı ≥ 0
    assert k18.a6(50)["1+1 aralığı (kesin)"] == (Fraction(41, 92), Fraction(51, 92))
    assert k18.a6(40)["1+1 aralığı (kesin)"] is None
