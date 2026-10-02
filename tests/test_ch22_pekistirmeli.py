"""Bölüm 22: kitaptaki değerlerle doğrulama."""
import random

import pytest

from yardimci import yukle

po = yukle("ch22-pekistirmeli-ogrenme/ornekler/pasif_ogrenme.py")
ao = yukle("ch22-pekistirmeli-ogrenme/ornekler/aktif_ogrenme.py")


def test_kitap_denemeleri():
    ilk = dict(reversed(po.odul_kalan(po.KITAP_DENEMELERI[0])))     # her durumun ilk ziyareti
    assert ilk[(1, 1)] == pytest.approx(0.76)
    kalanlar = po.odul_kalan(po.KITAP_DENEMELERI[0])
    assert [round(g, 2) for s, g in kalanlar if s == (1, 2)] == [0.80, 0.88]
    assert [round(g, 2) for s, g in kalanlar if s == (1, 3)] == [0.84, 0.92]
    adp = po.PasifADP()
    for d in po.KITAP_DENEMELERI:
        adp.ogren(d)
    assert adp.N_sa[((3, 3), "Sağ")] == 4
    assert adp.P((4, 3), (3, 3), "Sağ") == pytest.approx(0.5) and adp.P((3, 2), (3, 3), "Sağ") == pytest.approx(0.5)
    td = po.PasifTD(alfa=lambda n: 1.0)
    td.Ud[(1, 3)], td.Ud[(2, 3)] = 0.84, 0.96
    td.guncelle((1, 3), -0.04, (2, 3))
    assert td.U((1, 3)) == pytest.approx(0.92)                                # α = 1: tam olarak hedefe


def test_pasif_yontemler_yakinsar():
    sonuc, ajanlar = po.karsilastir((300,))
    for ad in ("doğrudan", "ADP"):
        assert ajanlar[ad].U((1, 1)) == pytest.approx(po.GERCEK_U[(1, 1)], abs=0.03)
    assert ajanlar["TD"].U((1, 1)) == pytest.approx(po.GERCEK_U[(1, 1)], abs=0.05)
    assert sonuc[300]["ADP"] < 0.1


def test_aktif_ogrenme():
    kesifci = ao.egit(ao.ADPAjani(), 200, tohum=0, kontrol=(200,))
    assert kesifci[200] < 0.05
    acgozlu = ao.egit(ao.ADPAjani(kesif=False), 200, tohum=0, kontrol=(200,))
    assert acgozlu[200] > kesifci[200]
    glie = ao.egit(ao.QAjani(kesif="glie"), 500, tohum=0, kontrol=(500,))
    assert glie[500] < 0.05
    assert ao.politika_kaybi(ao.DUNYA.acgozlu(ao.GERCEK_U)) == pytest.approx(0, abs=1e-9)


def test_islev_yaklasimi_ve_politika_aramasi():
    yp = yukle("ch22-pekistirmeli-ogrenme/ornekler/yaklasik_ve_politika.py")
    import numpy as np
    theta = np.array([0.5, 0.2, 0.1])
    assert yp.U_hat(theta, (1, 1)) == pytest.approx(0.8)                       # kitap
    yeni = yp.delta_kurali(theta, (1, 1), 0.4, alfa=0.1)
    assert yeni == pytest.approx(theta - 0.04)                                 # hepsi 0.4α azalır
    k22 = yukle("ch22-pekistirmeli-ogrenme/cozumler/alistirma_kod.py")
    a8 = k22.a8()
    assert a8["(1, x, y, hedefe uzaklık)"] == pytest.approx(a8["(1, x, y)"])   # uzaklık doğrusal birleşim
    assert a8["(1, x, y, uzaklık, −1'e komşu mu)"] < a8["(1, x, y)"]
    assert yp.reinforce(bolum=1500, kontrol=(1500,))[1500] < 0.05
