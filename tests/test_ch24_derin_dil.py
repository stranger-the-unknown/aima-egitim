"""Bölüm 24: gömmeler, dikkat ve kod çözme özelliklerinin doğrulanması."""
import numpy as np
import pytest

from yardimci import yukle

gm = yukle("ch24-derin-dil/ornekler/gomme.py")
dk = yukle("ch24-derin-dil/ornekler/dikkat.py")
kc = yukle("ch24-derin-dil/ornekler/kod_cozme.py")
k24 = yukle("ch24-derin-dil/cozumler/alistirma_kod.py")


def test_gommeler():
    I = np.eye(3)
    assert gm.kosinus(I[0], I[1]) == 0.0                                   # one-hot benzerlik taşımaz
    sozcukler, M = gm.birlikte_gecme(gm.DERLEM)
    V = gm.ppmi_svd(M)
    assert gm.en_yakinlar("kedi", sozcukler, V)[0][0] == "köpek"
    assert gm.en_yakinlar("araba", sozcukler, V)[0][0] == "otobüs"
    G = gm.yapay_gommeler()
    assert gm.benzetme(G, "Atina", "Yunanistan", "Oslo") == "Norveç"        # kitaptaki benzetme


def test_dikkat():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(6, 8))
    W = [rng.normal(0, 0.35, (8, 8)) for _ in range(3)]
    A, C = dk.oz_dikkat(X, *W)
    assert np.allclose(A.sum(axis=1), 1)
    p = rng.permutation(6)
    assert np.allclose(dk.oz_dikkat(X[p], *W)[1], C[p])                    # sıraya duyarsız
    P = dk.konum_kodlamasi(6, 8)
    assert not np.allclose(dk.oz_dikkat(X[p] + P, *W)[1], dk.oz_dikkat(X + P, *W)[1][p])
    Am, _ = dk.oz_dikkat(X, *W, maske=True)
    assert np.allclose(np.triu(Am, 1), 0)
    _, sonra = dk.olcek_etkisi(256)
    assert sonra == pytest.approx(1.0, abs=0.1)
    a5 = k24.a5()
    assert a5["olasılıklar"] == pytest.approx([np.e ** 2 / (2 * np.e ** 2 + 1), 1 / (2 * np.e ** 2 + 1), np.e ** 2 / (2 * np.e ** 2 + 1)])
    a6 = k24.a6()
    assert a6[5] == pytest.approx(a6["aynı uzaklık, farklı yer"])          # yalnızca uzaklığa bağlı


def test_kod_cozme():
    g, pg = kc.acgozlu()
    s, ps = kc.isin_aramasi(2)
    assert g[:2] == ["La", "entrada"] and s[:2] == ["La", "puerta"]
    assert ps > pg
    assert kc.isin_aramasi(1) == (g, pg)                                    # b = 1 açgözlüdür
    assert k24.a9()["sol + sağ bağlam"][0][0] == "süt"
