"""Bölüm 19: kitaptaki değerlerle doğrulama."""
import math
import random

import numpy as np
import pytest

from yardimci import yukle

ka = yukle("ch19-ogrenme-orneklerden/ornekler/karar_agaci.py")
dm = yukle("ch19-ogrenme-orneklerden/ornekler/dogrusal_modeller.py")
ms = yukle("ch19-ogrenme-orneklerden/ornekler/model_secimi.py")
po = yukle("ch19-ogrenme-orneklerden/ornekler/parametrik_olmayan.py")
tp = yukle("ch19-ogrenme-orneklerden/ornekler/topluluk.py")
k19 = yukle("ch19-ogrenme-orneklerden/cozumler/alistirma_kod.py")


def test_restoran_verisi_ve_entropi():
    assert len(ka.RESTORAN) == 12 and sum(y for _, y in ka.RESTORAN) == 6
    assert math.prod(len(v) for v in ka.NITELIKLER.values()) == 9216
    assert all(ka.gercek_agac(x) == y for x, y in ka.RESTORAN)          # Şekil 19.3 ile 19.2 tutarlı
    assert ka.entropi([0.5, 0.5]) == pytest.approx(1) and ka.entropi([0.25] * 4) == pytest.approx(2)
    assert ka.B(0.99) == pytest.approx(0.08, abs=0.005)


def test_bilgi_kazanci_ve_ogrenilen_agac():
    assert ka.kazanc("Pat", ka.RESTORAN) == pytest.approx(0.541, abs=1e-3)
    assert ka.kazanc("Type", ka.RESTORAN) == pytest.approx(0.0, abs=1e-12)
    assert max(ka.SIRA, key=lambda a: ka.kazanc(a, ka.RESTORAN)) == "Pat"
    agac = ka.agac_ogren(ka.RESTORAN, ka.SIRA)
    beklenen = ("Pat", {"None": False, "Some": True, "Full": ("Hun", {
        "Yes": ("Type", {"French": True, "Italian": False, "Thai": ("Fri", {"Yes": True, "No": False}), "Burger": True}),
        "No": False})})
    assert agac == beklenen                                               # Şekil 19.6
    assert all(ka.siniflandir(agac, x) == y for x, y in ka.RESTORAN)


def test_ki_kare_ve_karar_listesi():
    assert ka.ki_kare_3_esik(0.05) == pytest.approx(7.82, abs=0.01)
    assert ka.ki_kare_3_esik(0.01) == pytest.approx(11.35, abs=0.01)
    assert k19.ki_kare_kuyruk(7.8147, 3) == pytest.approx(0.05, abs=1e-4)
    assert k19.ki_kare_kuyruk(5.9915, 2) == pytest.approx(0.05, abs=1e-4)
    liste = ka.karar_listesi_ogren(ka.RESTORAN)
    assert all(ka.liste_siniflandir(liste, x) == y for x, y in ka.RESTORAN)
    assert all(len(test) <= 2 for test, _ in liste)


def test_ogrenme_egrisi_artar():
    e = ka.ogrenme_egrisi(boyutlar=(5, 20, 80), deneme=10)
    assert e[5] < e[20] < e[80] and e[80] > 0.9


def test_dogrusal_regresyon():
    x, y = dm.ev_verisi()
    w0, w1 = dm.kapali_bicim(x, y)
    assert np.polyfit(x, y, 1) == pytest.approx([w1, w0])
    g0, g1 = dm.gradyan_inisi(x, y)
    assert (g0, g1) == pytest.approx((w0, w1), rel=1e-6)
    X = np.random.default_rng(0).normal(size=(50, 3))
    yy = 1 + X @ np.array([2.0, -1.0, 0.5])
    assert dm.normal_denklemler(X, yy) == pytest.approx([1, 2, -1, 0.5])


def test_duzenlilestirme_ve_siniflandirma():
    s = k19.a8()
    assert s[0.3][0] >= 5 and s[0.3][1] == 0                               # L1 seyrek, L2 değil
    X, y = dm.sismik_veri()
    X1 = np.column_stack([np.ones(len(X)), X])
    assert np.all(dm.esik(X1 @ np.array([-4.9, 1.7, -1])) == y)
    w, adim = dm.algilayici(X, y)
    assert np.all(dm.esik(X1 @ w) == y)
    w, (mu, sd) = dm.lojistik_regresyon(X, y)
    olas = dm.lojistik(np.column_stack([np.ones(len(X)), (X - mu) / sd]) @ w)
    assert np.mean((olas >= 0.5) == y) == 1.0


def test_model_secimi_ve_pac():
    en_iyi, tablo = ms.model_secimi(*ms.polinom_veri())
    egitim = [tablo[d][0] for d in sorted(tablo)]
    assert all(a >= b - 1e-12 for a, b in zip(egitim, egitim[1:]))         # eğitim hatası azalır
    assert 2 <= en_iyi <= 6 and tablo[12][1] > tablo[en_iyi][1]
    assert ms.pac_ornek_sayisi(0.1, 0.05, math.log(1000)) == math.ceil((math.log(20) + math.log(1000)) / 0.1)
    assert ms.baglac_sayisi(3, 1) == 7


def test_boyutlarin_laneti():
    assert ms.komsuluk_kenari(2) == pytest.approx(0.003, abs=0.0005)
    assert ms.komsuluk_kenari(3) == pytest.approx(0.02, abs=0.003)
    assert ms.komsuluk_kenari(17) == pytest.approx(0.5, abs=0.02)
    assert ms.komsuluk_kenari(200) == pytest.approx(0.94, abs=0.005)
    assert ms.dis_kabuk_orani(1) == pytest.approx(0.02) and ms.dis_kabuk_orani(200) > 0.98


def test_parametrik_olmayan():
    X, y = po.gurultulu_veri()
    assert po.birini_disarida_birak(X, y, 5) > po.birini_disarida_birak(X, y, 1)
    rng = np.random.default_rng(5)
    P = rng.random((500, 3))
    agac = po.kd_kur(P)
    for _ in range(30):
        q = rng.random(3)
        assert po.kd_en_yakin(agac, P, q)[1] == int(np.argmin(np.linalg.norm(P - q, axis=1)))
    x, z = np.array([0.8, -1.2]), np.array([1.5, 0.4])
    assert float(po.F(x)[0] @ po.F(z)[0]) == pytest.approx(float(x @ z) ** 2)
    Xc, yc = po.cember_verisi()
    assert not po.algilayici_ayirir_mi(Xc, yc) and po.algilayici_ayirir_mi(po.F(Xc), yc)


def test_topluluk():
    assert tp.cogunluk_dogrulugu(5, 0.75) == pytest.approx(0.896, abs=1e-3)      # kitap: %89
    assert tp.cogunluk_dogrulugu(17, 0.75) == pytest.approx(0.99, abs=0.005)     # kitap: %99
    a, b = tp.rwm_siniri(0, 10, 0.5)
    assert (round(a, 2), round(b, 1)) == (1.39, 4.6)
    a, b = tp.rwm_siniri(0, 10, 0.75)
    assert (round(a, 2), round(b, 1)) == (1.15, 9.2)
    s = tp.rwm_benzetim()
    assert s["M"] <= s["sınır"]
    sonuc = tp.ogrenme_karsilastirmasi(deneme=3, Klar=(1, 5))
    assert sonuc[5]["test"] > sonuc[1]["test"]


def test_cozumler():
    assert k19.a3()["kök"] != "Pat"
    a5 = k19.a5()
    assert a5["Kimlik"][0] > a5["Pat"][0] and a5["Kimlik"][2] < a5["Pat"][2]   # kazanç oranı düzeltir
    a6 = k19.a6(deneme=3)
    assert a6["budanmış"][1] > a6["budamasız"][1] and a6["budanmış"][2] < a6["budamasız"][2]
    a9 = k19.a9()
    assert a9["(x₁, x₂, x₁² + x₂²)"] and not a9["girdi (x₁, x₂)"]
