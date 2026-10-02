"""Bölüm 20: kitaptaki değerlerle doğrulama."""
import math
from fractions import Fraction

import numpy as np
import pytest

from yardimci import yukle

io = yukle("ch20-olasiliksal-ogrenme/ornekler/istatistiksel_ogrenme.py")
em = yukle("ch20-olasiliksal-ogrenme/ornekler/em_algoritmasi.py")
nb = yukle("ch20-olasiliksal-ogrenme/ornekler/naif_bayes.py")
sm = yukle("ch20-olasiliksal-ogrenme/ornekler/surekli_modeller.py")
k20 = yukle("ch20-olasiliksal-ogrenme/cozumler/alistirma_kod.py")


def test_seker_torbalari():
    assert io.bayes_tahmini([]) == Fraction(1, 2)
    assert io.bayes_tahmini(["limon"]) == Fraction(13, 20)                   # 0.65
    assert float(io.bayes_tahmini(["limon"] * 3)) == pytest.approx(0.8, abs=0.01)
    assert io.sonsal(["limon"]) == {"h1": 0, "h2": Fraction(1, 10), "h3": Fraction(2, 5), "h4": Fraction(3, 10), "h5": Fraction(1, 5)}
    assert io.map_hipotezi(["limon"]) == "h3" and io.map_hipotezi(["limon"] * 2) == "h4"
    assert all(io.map_hipotezi(["limon"] * n) == "h5" for n in range(3, 11))
    tahminler = [io.bayes_tahmini(["limon"] * n) for n in range(11)]
    assert all(a < b for a, b in zip(tahminler, tahminler[1:]))              # tekdüze artar
    veri = ["limon"] * 3
    assert min(io.TORBALAR, key=lambda h: io.mdl_bitleri(h, veri)) == io.map_hipotezi(veri)


def test_en_buyuk_olabilirlik_ve_beta():
    assert io.ml_theta(7, 3) == pytest.approx(0.7)
    t = np.linspace(0.01, 0.99, 99)
    assert t[np.argmax([io.log_olabilirlik(x, 7, 3) for x in t])] == pytest.approx(0.7)
    ml = io.ambalaj_ml({("kiraz", "kırmızı"): 30, ("kiraz", "yeşil"): 10, ("limon", "kırmızı"): 6, ("limon", "yeşil"): 54})
    assert ml == pytest.approx({"θ": 0.4, "θ1": 0.75, "θ2": 0.1})
    assert io.beta_guncelle(1, 1, ["kiraz"] * 2) == (3, 1)
    assert io.beta_guncelle(3, 1, ["kiraz"] * 3 + ["limon"]) == (6, 2)
    assert io.beta_ortalama(30, 10) == pytest.approx(0.75)
    assert io.beta_varyans(30, 10) < io.beta_varyans(6, 2) < io.beta_varyans(3, 1)


def test_em_kitap_degerleri():
    gecmis = em.em(em.BASLANGIC, 10)
    t1, L1 = gecmis[1]
    kitap = {"θ": 0.6124, "F1": 0.6684, "W1": 0.6483, "H1": 0.6558, "F2": 0.3887, "W2": 0.3817, "H2": 0.3827}
    for k, v in kitap.items():
        assert t1[k] == pytest.approx(v, abs=5e-5)
    assert gecmis[0][1] == pytest.approx(-2044, abs=1) and L1 == pytest.approx(-2021, abs=1)
    assert em.log_olabilirlik(em.GERCEK) == pytest.approx(-1982.214, abs=1e-3)
    assert gecmis[10][1] > em.log_olabilirlik(em.GERCEK)                    # 10. yinelemede gerçeği geçer
    L = [l for _, l in gecmis]
    assert all(b >= a for a, b in zip(L, L[1:]))                             # EM olabilirliği azaltmaz
    assert k20.a7()["273 şekerin katkısı"] == pytest.approx(0.22797, abs=1e-5)


def test_tanimlanabilirlik_ve_parametre_sayisi():
    t1, L1 = em.iki_nitelik_em({"θ": 0.6, "F1": 0.6, "W1": 0.6, "F2": 0.4, "W2": 0.4})
    t2, L2 = em.iki_nitelik_em({"θ": 0.3, "F1": 0.9, "W1": 0.5, "F2": 0.4, "W2": 0.6})
    assert L1 == pytest.approx(L2, abs=1e-6) and abs(t1["θ"] - t2["θ"]) > 0.1
    assert em.kalp_hastaligi() == (78, 708)
    s = k20.a8()
    assert s["kitabın başlangıcı"][1] == pytest.approx(s["ters başlangıç"][1])
    assert s["simetrik (hepsi 0.5)"][1] < s["kitabın başlangıcı"][1]


def test_gauss_karisimi():
    X, (gw, gmu, _) = em.karisim_ornekle()
    w, mu, Sigma, L = em.gauss_karisimi_em(X, 3)
    sira = np.argsort(mu[:, 0])
    assert mu[sira] == pytest.approx(gmu, abs=0.03)
    assert w[sira] == pytest.approx(gw, abs=0.05)
    assert all(b >= a - 1e-6 for a, b in zip(L, L[1:]))
    a9 = k20.a9()
    assert max(a9, key=lambda k: a9[k][1]) == 3                              # test olabilirliği k = 3'te en iyi


def test_naif_bayes():
    model = nb.naif_bayes_ogren(nb.ka.RESTORAN, nb.ka.NITELIKLER)
    assert sum((nb.naif_bayes_sonsal(model, x) >= 0.5) == y for x, y in nb.ka.RESTORAN) >= 10
    e = nb.ogrenme_egrileri(boyutlar=(10, 80), deneme=5)
    assert e[80][1] > e[80][0]                                               # gerçek fonksiyon bir ağaç
    s = k20.a5()
    assert s[1] == pytest.approx(0.4) and s[10] > 0.999                      # kopyalar aşırı güven üretir


def test_surekli_modeller():
    x = np.random.default_rng(0).normal(5, 2, 200)
    mu, s = sm.gauss_ml(x)
    assert mu == pytest.approx(np.mean(x)) and s == pytest.approx(np.std(x))
    rng = np.random.default_rng(1)
    xv = rng.uniform(-3, 3, 20)
    yv = 1.5 * xv + rng.normal(0, 1, 20)
    tN, vN = sm.bayes_regresyon(xv, yv, 1.0)
    tS, vS = sm.bayes_regresyon_sayisal(xv, yv, 1.0)
    assert tN == pytest.approx(tS, abs=1e-4) and vN == pytest.approx(vS, rel=1e-3)
    dar = rng.uniform(-0.1, 0.1, 20)
    assert sm.bayes_regresyon(dar, dar, 1.0)[1] > 10 * vN                    # dar veri eğimi az kısıtlar
    assert sm.tahmin_varyansi(10, 1, vN) > sm.tahmin_varyansi(0.5, 1, vN)
