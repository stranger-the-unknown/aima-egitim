"""Bölüm 21: kitaptaki değerlerle ve tutarlılık kontrolleriyle doğrulama."""
import numpy as np
import pytest

from yardimci import yukle

hg = yukle("ch21-derin-ogrenme/ornekler/hesap_grafigi.py")
cnn = yukle("ch21-derin-ogrenme/ornekler/cnn.py")
me = yukle("ch21-derin-ogrenme/ornekler/mlp_egitim.py")
rnn = yukle("ch21-derin-ogrenme/ornekler/rnn.py")
ok = yukle("ch21-derin-ogrenme/ornekler/otokodlayici.py")
k21 = yukle("ch21-derin-ogrenme/cozumler/alistirma_kod.py")


def test_aktivasyonlar_ve_softmax():
    x = np.linspace(-4, 4, 17)
    assert np.allclose(np.tanh(x), 2 * hg.sigmoid(2 * x) - 1)
    assert np.allclose((hg.softplus(x + 1e-6) - hg.softplus(x - 1e-6)) / 2e-6, hg.sigmoid(x), atol=1e-6)
    assert np.round(hg.softmax([5, 2, 0, -2]), 3).tolist() == [0.946, 0.047, 0.006, 0.001]   # kitap
    assert hg.softmax([1.7, 0])[0] == pytest.approx(hg.sigmoid(1.7))
    P, Q = [0.7, 0.2, 0.1], [0.5, 0.3, 0.2]
    assert hg.capraz_entropi(P, Q) == pytest.approx(hg.entropi(P) + hg.kl(P, Q))


def test_geri_yayilim_sayisal_gradyanla():
    for x1, x2, y in ((1.0, 0.5, 1.0), (-0.3, 2.0, 0.0)):
        g, s = hg.geri_yayilim(hg.AGIRLIKLAR, x1, x2, y), hg.sayisal_gradyan(hg.AGIRLIKLAR, x1, x2, y)
        for k in g:
            assert g[k] == pytest.approx(s[k], abs=1e-7)
    assert hg.kaybolan_gradyan(20) <= 0.25 ** 20


def test_evrisim():
    x, k = [5, 6, 6, 2, 5, 6, 5], [1, -1, 1]
    assert cnn.evrisim_1b(x, k, adim=2).tolist() == [5, 9, 4]                  # Şekil 21.4
    assert (cnn.evrisim_matrisi(7, k, 2) @ x).tolist() == [5, 9, 4]            # (21.9)
    assert len(cnn.evrisim_1b(x, k, 1, 1)) == len(x)
    assert [cnn.alici_alan(n) for n in (1, 2, 3)] == [3, 5, 7]
    assert cnn.havuzla([1, 3, 2, 8]).tolist() == [3, 8] and cnn.havuzla([1, 3, 2, 8], tur="ort").tolist() == [2, 5]
    assert k21.cikti_boyutu(224, 7, 2, 3) == 112 and k21.cikti_boyutu(32, 3, 1, 1) == 32
    z = np.array([0.5, 1.2, 0.0, 2.0])
    assert cnn.artik_katman(z, np.zeros((4, 4)), np.zeros(4)).tolist() == z.tolist()


def test_mlp():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    y = np.array([0, 1, 1, 0])
    ag = me.MLP([2, 8, 2], tohum=1)
    ag.egit(X, y, tur=2000, toplu=4, alfa=0.5)
    assert ag.dogruluk(X, y) == 1.0
    dogrusal = me.MLP([2, 2], tohum=1)
    dogrusal.egit(X, y, tur=500, toplu=4, alfa=0.5)
    assert dogrusal.dogruluk(X, y) <= 0.75                                      # XOR doğrusal ayrılamaz
    assert k21.a7()["çıktı"] == [0, 1, 1, 0]
    Zn = me.toplu_normallestir(np.random.default_rng(0).normal(5, 3, (64, 3)))
    assert np.allclose(Zn.mean(axis=0), 0, atol=1e-9) and np.allclose(Zn.std(axis=0), 1, atol=1e-3)
    assert k21.a9()["aynı mı"]
    assert me.ilk_katman_gradyani(30, True) > 1e10 * me.ilk_katman_gradyani(30, False)


def test_gradyanlar_derinlikte():
    s = k21.a6()
    assert s[50][0] < 1e-20 < 1 < s[50][1]                                      # sigmoid kaybolur, ReLU kaybolmaz
    W, _, _ = rnn.rastgele_rnn(8, 0.5)
    zs, _ = rnn.rnn_ileri(W, np.ones(8), np.ones(8), np.random.default_rng(1).normal(0, 0.5, 41))
    g = rnn.gecmise_gradyan(W, zs)
    assert g[39] < 1e-10 < g[0]
    assert rnn.lstm_bellegi(1.0, 30) == 1.0 and rnn.lstm_bellegi(0.5, 30) < 1e-8


def test_dropout_ve_otokodlayici():
    s = k21.a8(deneme=100_000)
    assert s["ortalama çıktı"] == pytest.approx(s["gerçek"], abs=0.02)
    rng = np.random.default_rng(0)
    W_gercek = rng.normal(size=(10, 2)) * np.array([3.0, 1.5])
    X = ok.ppca_ornekle(1000, W_gercek, 0.3, rng)
    _, P = ok.pca(X, 2)
    W = ok.dogrusal_otokodlayici(X, 2)
    assert np.all(ok.temel_acilar(W.T, P) < 0.1)                                # aynı alt uzay
    a10 = k21.a10()
    for m in (1, 2):
        assert a10[m][0] == pytest.approx(a10[m][1], rel=1e-3)
