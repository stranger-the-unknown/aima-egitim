"""Bölüm 26: lokalizasyon, hareket planlama, denetim ve insan–robot etkileşimi özelliklerinin doğrulanması."""
import math

import numpy as np
import pytest

from yardimci import yukle

lk = yukle("ch26-robotik/ornekler/lokalizasyon.py")
pl = yukle("ch26-robotik/ornekler/planlama.py")
kn = yukle("ch26-robotik/ornekler/kontrol.py")
ir = yukle("ch26-robotik/ornekler/insan_robot.py")


def test_hareket_ve_algilayici_modelleri():
    X = lk.hareket(np.array([2.0, 1.0, 0.0]), 1.0, 0.2)
    assert X == pytest.approx([3.0, 1.0, 0.2])                              # X + (vΔt cos θ, vΔt sin θ, ωΔt)
    z = lk.isaret_olcumu(np.array([0.0, 0.0, 0.0]), (3.0, 4.0))
    assert z == pytest.approx([5.0, math.atan2(4, 3)])
    tarama = lk.isin_izle(np.array([[6.0, 1.0, 0.0], [14.0, 1.0, math.pi]]))
    assert tarama[0] == pytest.approx(tarama[1])                            # ayna pozları aynı taramayı verir


def test_mcl_ve_ekf():
    s = lk.mcl_deneyi()
    assert s[3][1] > 0.05 and s[3][2] > 0.05                                # iki tepeli inanç
    assert s[-1][1] > 0.95                                                  # girinti görülünce tek tepe
    e = lk.ekf_deneyi()
    assert e[3][2] < e[2][2]                                                # işaret görülünce belirsizlik azalır
    assert e[-1][2] > e[-4][2]                                              # görmeyince yeniden artar
    d = lk.dogrusallastirma()
    assert abs(d["Taylor std"] - d["gerçek std"]) > 0.3                     # doğrusallaştırma kovaryansı bozar


def test_c_uzayi_ve_kinematik():
    K = pl.c_engeli()
    assert len(K) == 5                                                      # beş kenarlı çokgen (Şekil 26.11)
    for x in np.arange(0.05, 8, 0.3):
        for y in np.arange(0.05, 5, 0.3):
            assert pl.ucgen_carpisir((x, y)) == pl.icinde_mi((x, y), K)
    for t1, t2 in pl.ters_kinematik(0.866, 1.5):
        assert pl.ileri_kinematik(t1, t2)[1] == pytest.approx((0.866, 1.5), abs=1e-9)
    assert len(pl.ters_kinematik(0.866, 1.5)) == 2 and pl.ters_kinematik(2.5, 0) == []


def test_planlayicilar():
    t1, t2, C = pl.kol_c_uzayi()
    bas, hedef = (0, list(t2).index(0)), (list(t1).index(120), list(t2).index(0))
    _, yol = pl.izgara_en_kisa(C, bas, hedef)
    assert yol is not None and all(not C[c] for c in yol)
    assert any(pl.kol_carpisir(math.radians(a), 0.0) for a in range(0, 121, 5))
    _, en_iyi = pl.gorunurluk_cizgesi()
    assert en_iyi == pytest.approx(13.715, abs=1e-3)
    yol, uzunluk, _ = pl.prm(30)
    assert uzunluk >= en_iyi and all(pl.serbest_dogru(yol[i], yol[i + 1]) for i in range(len(yol) - 1))
    r = pl.rrt_cift_yonlu()
    k = pl.kisalt(r)
    assert en_iyi <= pl.yol_uzunlugu(k) <= pl.yol_uzunlugu(r)
    T = pl.yorunge_optimizasyonu()
    assert pl.en_kucuk_aciklik(T) > 1.3 > pl.en_kucuk_aciklik(np.linspace((0, 0), (10, 0), 51))
    kivrik = np.linspace((0, 0), (10, 0), 51) + np.stack([np.zeros(51), np.sin(np.linspace(0, 3 * np.pi, 51))], 1)
    assert pl.yol_uzunlugu(pl.yorunge_optimizasyonu(baslangic=kivrik, engeller=[])) == pytest.approx(10.0, abs=1e-3)


def test_denetim():
    assert kn.ozet(*kn.benzet(1.0))["son 10 s salınım"] > 1.9                # P: sonsuz salınım
    assert kn.ozet(*kn.benzet(0.3, 0.8))["son 10 s salınım"] < 1e-3          # PD: oturur
    assert kn.ozet(*kn.benzet(0.3, 0.8, d=-0.05, sure=200))["son hata"] == pytest.approx(0.05 / 0.3, abs=1e-3)
    assert abs(kn.ozet(*kn.benzet(0.3, 0.8, 0.05, d=-0.05, sure=200))["son hata"]) < 1e-3
    K = kn.lqr_ayrik(*kn.cift_integrator(0.001), np.diag([1.0, 0.0]), np.array([[1.0]]))
    assert K.ravel() == pytest.approx([1.0, math.sqrt(2)], abs=0.01)


def test_insan_robot():
    b = ir.amac_cikarimi()
    assert b[-1]["pencere"] > 0.95 and b[1]["koridor"] < b[0]["koridor"]
    s = ir.klonlama_ve_dagger()
    assert s["klonlama"][0][0] == pytest.approx(0.0, abs=1e-3) and s["klonlama"][1] > 0.3
    assert s["DAGGER 1"][0][0] == pytest.approx(-0.5, abs=1e-3) and s["DAGGER 1"][1] == 0.0
    adimlar = ir.bacak_afsm([0.0, 2.5])
    assert adimlar[0][1] == 1 and adimlar[1][1] == 3
    assert ir.merkez_destekte_mi(["SağÖn", "SağArka", "SolOrta"])
    assert not ir.merkez_destekte_mi(["SolÖn", "SolOrta", "SolArka"])
