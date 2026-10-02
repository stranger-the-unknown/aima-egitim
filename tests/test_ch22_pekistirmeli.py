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
